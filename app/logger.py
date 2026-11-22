"""
Professional, visual, and elegant dual-sink logging subsystem.
Features colorized console formatting with badges and persistent rotating file logging.
"""
import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import time
from typing import Optional

# ANSI Color Codes for Terminal Styling
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

COLOR_CYAN = "\033[36m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_RED = "\033[31m"
COLOR_MAGENTA = "\033[35m"
COLOR_BLUE = "\033[34m"
COLOR_GRAY = "\033[90m"

BG_GREEN = "\033[42m\033[30m"
BG_RED = "\033[41m\033[37m"
BG_BLUE = "\033[44m\033[37m"


class ConsoleColorFormatter(logging.Formatter):
    """Formats log records with elegant ANSI colors, badges, and icons for terminal viewing."""

    LEVEL_BADGES = {
        logging.DEBUG: f"{COLOR_GRAY}[DEBUG]{RESET}",
        logging.INFO: f"{COLOR_CYAN}{BOLD}[INFO ]{RESET}",
        logging.WARNING: f"{COLOR_YELLOW}{BOLD}[WARN ]{RESET}",
        logging.ERROR: f"{COLOR_RED}{BOLD}[ERROR]{RESET}",
        logging.CRITICAL: f"{BG_RED}{BOLD}[FATAL]{RESET}",
    }

    def format(self, record: logging.LogRecord) -> str:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))
        millis = int(record.msecs)
        time_str = f"{COLOR_GRAY}{timestamp}.{millis:03d}{RESET}"

        badge = self.LEVEL_BADGES.get(record.levelno, f"[{record.levelname}]")
        logger_name = f"{COLOR_MAGENTA}{DIM}{record.name:<26}{RESET}"

        # Indent multi-line messages cleanly
        message = record.getMessage()
        if "\n" in message:
            message = message.replace("\n", "\n" + " " * 38)

        return f"{time_str} {badge} {logger_name} {message}"


class PlainFileFormatter(logging.Formatter):
    """Clean, uncolorized structured formatter for permanent file storage in logs/app.log."""

    def format(self, record: logging.LogRecord) -> str:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))
        millis = int(record.msecs)
        return f"{timestamp}.{millis:03d} [{record.levelname:<5}] [{record.name}] {record.getMessage()}"


def setup_logging(
    log_level: int = logging.INFO,
    log_file: str = "logs/app.log",
) -> None:
    """
    Initialize the dual-sink logging system:
    1. Rich ANSI colorized output to stdout.
    2. Persistent rotating log file at logs/app.log (5MB max per file, 5 backups).
    """
    # Ensure logs/ directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicates on re-init
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # 1. Console Handler (Colorized)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(ConsoleColorFormatter())
    root_logger.addHandler(console_handler)

    # 2. Rotating File Handler (Plain text, persistent)
    try:
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(PlainFileFormatter())
        root_logger.addHandler(file_handler)
    except Exception as e:
        sys.stderr.write(f"Warning: Could not initialize file logger at {log_file}: {e}\n")

    # Mute noisy third-party loggers slightly
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


# Visual Helper Loggers for Posting Lifecycle
logger = logging.getLogger("posting.engine")


def log_broadcast_start(platforms_count: int, message: str, cta_url: str, is_mock: bool) -> None:
    """Print an eye-catching dispatch banner when posting starts."""
    mode_tag = f"{COLOR_YELLOW}[MOCK MODE]{RESET}" if is_mock else f"{COLOR_GREEN}[LIVE PRODUCTION]{RESET}"
    short_msg = (message[:75] + "...") if len(message) > 75 else message

    logger.info(
        f"\n{COLOR_CYAN}┌{'─'*74}┐{RESET}\n"
        f"{COLOR_CYAN}│{RESET} {BOLD}🚀 INITIATING MULTI-PLATFORM BROADCAST{RESET} {mode_tag}\n"
        f"{COLOR_CYAN}│{RESET} {COLOR_GRAY}Target Platforms:{RESET} {BOLD}{platforms_count}{RESET} concurrently via asyncio.gather\n"
        f"{COLOR_CYAN}│{RESET} {COLOR_GRAY}Message:{RESET}          \"{short_msg}\"\n"
        f"{COLOR_CYAN}│{RESET} {COLOR_GRAY}CTA Link:{RESET}         {COLOR_BLUE}{cta_url}{RESET}\n"
        f"{COLOR_CYAN}└{'─'*74}┘{RESET}"
    )


def log_platform_dispatch_result(
    platform_name: str,
    status: str,
    url_or_error: Optional[str],
    elapsed_ms: float,
) -> None:
    """Log individual platform completion with visual checkmark / cross and latency."""
    if status == "success":
        icon = f"{COLOR_GREEN}✓{RESET}"
        status_badge = f"{COLOR_GREEN}{BOLD}SUCCESS{RESET}"
        info = f"{COLOR_BLUE}{url_or_error}{RESET}"
    else:
        icon = f"{COLOR_RED}✗{RESET}"
        status_badge = f"{COLOR_RED}{BOLD}FAILED {RESET}"
        info = f"{COLOR_GRAY}{url_or_error}{RESET}"

    time_badge = f"{COLOR_GRAY}({elapsed_ms:>5.1f}ms){RESET}"
    logger.info(f"  {icon} [{platform_name:<18}] {status_badge} {time_badge} ➔ {info}")


def log_broadcast_summary(
    total: int,
    succeeded: int,
    failed: int,
    total_ms: float,
) -> None:
    """Log the aggregate completion summary with timing."""
    if succeeded == total:
        status_color = COLOR_GREEN
        status_icon = "✨ ALL SUCCEEDED"
    elif succeeded > 0:
        status_color = COLOR_YELLOW
        status_icon = "⚡ PARTIAL SUCCESS"
    else:
        status_color = COLOR_RED
        status_icon = "⚠️ ALL FAILED"

    logger.info(
        f"{status_color}⚡ SUMMARY:{RESET} {BOLD}{status_icon}{RESET} "
        f"• {COLOR_GREEN}{succeeded} Succeeded{RESET} "
        f"• {COLOR_RED if failed > 0 else COLOR_GRAY}{failed} Failed{RESET} "
        f"• {COLOR_GRAY}Total Execution: {total_ms:.1f}ms{RESET}\n"
    )
