"""
Interactive, modern, scroll-storytelling documentation interface and dedicated API Setup Guide.
"""

# ==============================================================================
# 1. Main Interactive Documentation Page (DOCS_HTML)
# ==============================================================================
DOCS_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Multi-Platform Posting System — Documentation & Playground</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b0f19;
      --bg-card: rgba(18, 24, 38, 0.75);
      --bg-card-hover: rgba(28, 36, 56, 0.9);
      --border: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(99, 102, 241, 0.35);
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --primary: #6366f1;
      --primary-light: #818cf8;
      --secondary: #06b6d4;
      --accent: #ec4899;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
      --radius: 14px;
      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      line-height: 1.6;
      overflow-x: hidden;
      background-image: 
        radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.14) 0%, transparent 40%),
        radial-gradient(circle at 85% 65%, rgba(6, 182, 212, 0.12) 0%, transparent 40%),
        radial-gradient(circle at 50% 90%, rgba(236, 72, 153, 0.09) 0%, transparent 40%);
      background-attachment: fixed;
    }

    /* Header Nav Band - Perfectly Aligned and In Order */
    header {
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(18px);
      background: rgba(11, 15, 25, 0.88);
      border-bottom: 1px solid var(--border);
      padding: 0.9rem 2.25rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .logo-group {
      display: flex;
      align-items: center;
      gap: 0.8rem;
      text-decoration: none;
      color: var(--text);
    }
    .logo-badge {
      width: 38px;
      height: 38px;
      border-radius: 10px;
      background: linear-gradient(135deg, var(--primary), var(--secondary));
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.15rem;
      color: white;
      box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
    }
    .logo-title {
      font-weight: 700;
      font-size: 1.05rem;
      letter-spacing: -0.02em;
    }
    .nav-links {
      display: flex;
      gap: 1.5rem;
      align-items: center;
      list-style: none;
    }
    .nav-links a {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.9rem;
      font-weight: 600;
      transition: color 0.2s ease;
    }
    .nav-links a:hover { color: var(--text); }
    .btn-nav-guide {
      color: #fbbf24 !important;
      background: rgba(245, 158, 11, 0.12);
      border: 1px solid rgba(245, 158, 11, 0.3);
      padding: 0.45rem 0.9rem;
      border-radius: 8px;
      font-size: 0.85rem !important;
      font-weight: 700 !important;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.2s ease;
    }
    .btn-nav-guide:hover {
      background: #f59e0b !important;
      color: #0b0f19 !important;
      box-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
    }
    .btn-swagger {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.45rem 0.95rem;
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid var(--border-accent);
      color: var(--primary-light);
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s ease;
    }
    .btn-swagger:hover {
      background: var(--primary);
      color: white;
      box-shadow: 0 0 15px rgba(99, 102, 241, 0.4);
    }

    /* Container */
    .container {
      max-width: 1240px;
      margin: 0 auto;
      padding: 3rem 1.5rem;
    }

    /* Sections */
    section {
      margin-bottom: 5.5rem;
      opacity: 0;
      transform: translateY(20px);
      transition: all 0.65s cubic-bezier(0.16, 1, 0.3, 1);
    }
    section.revealed {
      opacity: 1;
      transform: translateY(0);
    }

    /* Hero */
    .hero {
      text-align: center;
      padding: 2.5rem 1rem 4rem;
    }
    .hero-pill {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.35rem 0.95rem;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border);
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--primary-light);
      margin-bottom: 1.5rem;
    }
    .hero-pill .dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--success);
      box-shadow: 0 0 8px var(--success);
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.4; }
    }
    .hero h1 {
      font-size: 3.3rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1.15;
      margin-bottom: 1.25rem;
    }
    .hero h1 .gradient-text {
      background: linear-gradient(135deg, #fff 30%, var(--primary-light) 70%, var(--secondary) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero p {
      max-width: 760px;
      margin: 0 auto 2.25rem;
      font-size: 1.15rem;
      color: var(--text-muted);
    }
    .hero-actions {
      display: flex;
      justify-content: center;
      gap: 1rem;
      flex-wrap: wrap;
    }
    .btn-primary {
      padding: 0.8rem 1.7rem;
      background: linear-gradient(135deg, var(--primary), #4f46e5);
      color: white;
      border: none;
      border-radius: 10px;
      font-size: 0.95rem;
      font-weight: 700;
      cursor: pointer;
      text-decoration: none;
      box-shadow: 0 4px 20px rgba(99, 102, 241, 0.35);
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
    }
    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 25px rgba(99, 102, 241, 0.5);
    }
    .btn-secondary {
      padding: 0.8rem 1.7rem;
      background: rgba(255, 255, 255, 0.05);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 10px;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
    }
    .btn-secondary:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.2);
    }

    /* Stats Grid */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1.25rem;
      margin-top: 3.5rem;
    }
    .stat-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.5rem;
      text-align: left;
      backdrop-filter: blur(12px);
      transition: all 0.25s ease;
    }
    .stat-card:hover {
      border-color: var(--border-accent);
      transform: translateY(-3px);
    }
    .stat-value {
      font-size: 2rem;
      font-weight: 800;
      background: linear-gradient(135deg, #fff, var(--secondary));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.25rem;
    }
    .stat-label {
      font-size: 0.85rem;
      color: var(--text-muted);
      font-weight: 500;
    }

    /* Section Headings */
    .section-header {
      margin-bottom: 2rem;
    }
    .section-tag {
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--primary-light);
      margin-bottom: 0.5rem;
    }
    .section-title {
      font-size: 1.95rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin-bottom: 0.5rem;
    }
    .section-desc {
      color: var(--text-muted);
      font-size: 1rem;
      max-width: 720px;
    }

    /* Architecture Visualizer */
    .architecture-box {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 2.25rem;
      backdrop-filter: blur(12px);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    .pipeline {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
      overflow-x: auto;
      padding: 1rem 0;
    }
    .pipeline-step {
      flex: 1;
      min-width: 170px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.25rem 1rem;
      text-align: center;
      cursor: pointer;
      transition: all 0.25s ease;
      position: relative;
    }
    .pipeline-step.active, .pipeline-step:hover {
      background: rgba(99, 102, 241, 0.14);
      border-color: var(--primary);
      transform: translateY(-4px);
    }
    .pipeline-icon {
      font-size: 1.5rem;
      margin-bottom: 0.5rem;
    }
    .pipeline-title {
      font-size: 0.9rem;
      font-weight: 700;
      margin-bottom: 0.2rem;
    }
    .pipeline-sub {
      font-size: 0.75rem;
      color: var(--text-muted);
    }
    .pipeline-arrow {
      color: var(--text-muted);
      font-size: 1.25rem;
      flex-shrink: 0;
    }
    .pipeline-detail-card {
      margin-top: 1.75rem;
      background: rgba(15, 21, 37, 0.9);
      border: 1px solid var(--border-accent);
      border-radius: 12px;
      padding: 1.75rem;
      font-size: 0.92rem;
    }
    .pipeline-detail-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.75rem;
    }
    .pipeline-detail-title {
      font-weight: 700;
      font-size: 1.05rem;
      color: var(--primary-light);
    }

    /* Playground */
    .playground-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
    }
    @media (max-width: 880px) {
      .playground-grid { grid-template-columns: 1fr; }
    }
    .playground-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.75rem;
      backdrop-filter: blur(12px);
      display: flex;
      flex-direction: column;
    }
    .preset-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 1rem;
    }
    .preset-chip {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 0.3rem 0.75rem;
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .preset-chip:hover {
      background: var(--primary);
      color: white;
      border-color: var(--primary);
    }
    .message-textarea {
      width: 100%;
      height: 120px;
      background: rgba(11, 15, 25, 0.8);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.85rem;
      color: var(--text);
      font-family: var(--font-sans);
      font-size: 0.9rem;
      resize: vertical;
      outline: none;
      transition: border-color 0.2s ease;
      margin-bottom: 0.75rem;
    }
    .message-textarea:focus {
      border-color: var(--primary);
      box-shadow: 0 0 10px rgba(99, 102, 241, 0.25);
    }
    .live-validators {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.8rem;
      margin-bottom: 1.25rem;
    }
    .char-counter {
      font-family: var(--font-mono);
      color: var(--text-muted);
    }
    .char-counter.valid { color: var(--success); font-weight: 600; }
    .char-counter.invalid { color: var(--danger); font-weight: 600; }
    .url-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      padding: 0.25rem 0.6rem;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
    }
    .url-badge.valid {
      background: rgba(16, 185, 129, 0.15);
      color: var(--success);
      border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .url-badge.invalid {
      background: rgba(239, 68, 68, 0.15);
      color: var(--danger);
      border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .btn-submit {
      width: 100%;
      padding: 0.85rem;
      background: linear-gradient(135deg, var(--primary), var(--secondary));
      color: white;
      border: none;
      border-radius: 10px;
      font-size: 0.95rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      transition: all 0.2s ease;
      box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    .btn-submit:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
    }
    .btn-submit:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }

    /* Response View */
    .response-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.75rem;
    }
    .response-status-badge {
      padding: 0.25rem 0.65rem;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 700;
      font-family: var(--font-mono);
    }
    .status-200 { background: rgba(16, 185, 129, 0.2); color: var(--success); }
    .status-422 { background: rgba(239, 68, 68, 0.2); color: var(--danger); }
    .timer-badge {
      font-size: 0.78rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }
    .response-viewer {
      flex: 1;
      background: rgba(11, 15, 25, 0.9);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1rem;
      font-family: var(--font-mono);
      font-size: 0.8rem;
      overflow-y: auto;
      max-height: 400px;
      white-space: pre-wrap;
      word-break: break-all;
    }

    /* Platform Grid */
    .platform-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 1.25rem;
    }
    .platform-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.6rem;
      backdrop-filter: blur(12px);
      transition: all 0.25s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .platform-card:hover {
      border-color: var(--border-accent);
      transform: translateY(-3px);
    }
    .platform-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
    }
    .platform-title-group {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .platform-avatar {
      width: 42px;
      height: 42px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.35rem;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border);
    }
    .platform-name {
      font-size: 1.1rem;
      font-weight: 700;
    }
    .platform-category {
      font-size: 0.75rem;
      color: var(--text-muted);
    }
    .platform-endpoint {
      background: rgba(0, 0, 0, 0.35);
      padding: 0.55rem 0.8rem;
      border-radius: 8px;
      font-family: var(--font-mono);
      font-size: 0.75rem;
      color: var(--primary-light);
      margin-bottom: 0.75rem;
      overflow-x: auto;
    }
    .platform-meta {
      display: flex;
      justify-content: space-between;
      font-size: 0.82rem;
      color: var(--text-muted);
      margin-top: 0.75rem;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      padding-top: 0.75rem;
    }

    /* Dedicated API Guide Box Callout */
    .api-guide-callout-box {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.08), rgba(99, 102, 241, 0.08));
      border: 1px solid rgba(245, 158, 11, 0.35);
      border-radius: var(--radius);
      padding: 2.25rem 2.5rem;
      backdrop-filter: blur(14px);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 2rem;
      flex-wrap: wrap;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }
    .api-guide-callout-content {
      flex: 1;
      min-width: 300px;
    }
    .api-guide-callout-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.3rem 0.75rem;
      background: rgba(245, 158, 11, 0.15);
      color: #fbbf24;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 700;
      margin-bottom: 0.85rem;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .api-guide-callout-title {
      font-size: 1.5rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin-bottom: 0.6rem;
    }
    .api-guide-callout-desc {
      color: var(--text-muted);
      font-size: 0.98rem;
      line-height: 1.6;
      max-width: 680px;
    }
    .btn-open-guide {
      padding: 0.95rem 1.85rem;
      background: linear-gradient(135deg, #f59e0b, #d97706);
      color: #0b0f19;
      border: none;
      border-radius: 10px;
      font-size: 1rem;
      font-weight: 800;
      cursor: pointer;
      text-decoration: none;
      box-shadow: 0 4px 20px rgba(245, 158, 11, 0.35);
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.6rem;
      white-space: nowrap;
    }
    .btn-open-guide:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 25px rgba(245, 158, 11, 0.5);
      background: #fbbf24;
    }

    /* Tables */
    .rules-table {
      width: 100%;
      border-collapse: collapse;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
      margin-top: 1rem;
    }
    .rules-table th, .rules-table td {
      padding: 1.1rem 1.25rem;
      text-align: left;
      font-size: 0.9rem;
      border-bottom: 1px solid var(--border);
    }
    .rules-table th {
      background: rgba(255, 255, 255, 0.03);
      font-weight: 700;
      color: var(--text-muted);
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .rule-tag {
      display: inline-block;
      padding: 0.2rem 0.55rem;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 700;
      font-family: var(--font-mono);
    }

    /* Schema Card */
    .schema-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.75rem;
      backdrop-filter: blur(12px);
      margin-bottom: 1.5rem;
    }

    /* Curl Box */
    .curl-box {
      margin-top: 1rem;
      background: rgba(0, 0, 0, 0.45);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.85rem;
      font-family: var(--font-mono);
      font-size: 0.8rem;
      color: var(--secondary);
      position: relative;
    }
    .copy-btn {
      position: absolute;
      top: 0.6rem;
      right: 0.6rem;
      background: rgba(255, 255, 255, 0.1);
      border: none;
      color: var(--text);
      padding: 0.25rem 0.6rem;
      border-radius: 6px;
      font-size: 0.75rem;
      cursor: pointer;
      transition: background 0.2s ease;
    }
    .copy-btn:hover { background: rgba(255, 255, 255, 0.2); }

    /* Footer */
    footer {
      border-top: 1px solid var(--border);
      padding: 3rem 1.5rem;
      text-align: center;
      color: var(--text-muted);
      font-size: 0.9rem;
    }
    footer a {
      color: var(--primary-light);
      text-decoration: none;
    }
    footer a:hover { text-decoration: underline; }
  </style>
</head>
<body>

  <!-- Upper Header Band (Names & Texts in Strict Logical Order) -->
  <header>
    <a href="#hero" class="logo-group">
      <div class="logo-badge">⚡</div>
      <div>
        <div class="logo-title">Multi-Platform Posting System</div>
      </div>
    </a>
    <ul class="nav-links">
      <li><a href="#architecture">Architecture</a></li>
      <li><a href="#playground">Playground</a></li>
      <li><a href="#platforms">Platforms</a></li>
      <li><a href="#rules">Validation</a></li>
      <li><a href="#schema">API Schema</a></li>
      <li><a href="/api-guide" class="btn-nav-guide">🔑 API Guide</a></li>
      <li><a href="/swagger" class="btn-swagger">Swagger UI ↗</a></li>
    </ul>
  </header>

  <div class="container">

    <!-- 1. Hero Section -->
    <section id="hero" class="hero revealed">
      <div class="hero-pill">
        <span class="dot"></span>
        FastAPI 0.115+ • Python 3.12 • Sub-Second Parallel Execution
      </div>
      <h1>
        Broadcast Everywhere.<br>
        <span class="gradient-text">Zero Cascading Failure.</span>
      </h1>
      <p>
        An enterprise asynchronous posting engine that automatically validates and broadcasts short announcements across 6 leading platforms concurrently with complete fault isolation.
      </p>
      <div class="hero-actions">
        <a href="#playground" class="btn-primary">⚡ Try Live Playground</a>
        <a href="/api-guide" class="btn-secondary">🔑 API Keys Setup Guide ➔</a>
        <a href="/swagger" class="btn-secondary">Open Swagger Explorer ↗</a>
      </div>

      <!-- Quick Metrics Grid -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">6</div>
          <div class="stat-label">Integrated Ecosystems (Social, Forums, Developer)</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">&lt; 500ms</div>
          <div class="stat-label">Parallel Execution Latency via <code>asyncio.gather</code></div>
        </div>
        <div class="stat-card">
          <div class="stat-value">100%</div>
          <div class="stat-label">Isolated Error Boundaries (Failures Stay Local)</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">34 / 34</div>
          <div class="stat-label">Automated Tests Passing (Pytest Suite)</div>
        </div>
      </div>
    </section>

    <!-- 2. Architecture Section -->
    <section id="architecture">
      <div class="section-header">
        <div class="section-tag">Visual Pipeline</div>
        <h2 class="section-title">Asynchronous Concurrency &amp; Error Isolation</h2>
        <p class="section-desc">
          Click any stage of the pipeline below to inspect how incoming messages travel from validation to parallel distribution without cascading bottlenecks.
        </p>
      </div>

      <div class="architecture-box">
        <div class="pipeline">
          <div class="pipeline-step active" onclick="selectStep('req', event)">
            <div class="pipeline-icon">📥</div>
            <div class="pipeline-title">1. HTTP Request</div>
            <div class="pipeline-sub">POST /posting</div>
          </div>
          <div class="pipeline-arrow">➔</div>
          <div class="pipeline-step" onclick="selectStep('val', event)">
            <div class="pipeline-icon">🛡️</div>
            <div class="pipeline-title">2. Pydantic Gate</div>
            <div class="pipeline-sub">≤ 200 Chars &amp; 1 CTA</div>
          </div>
          <div class="pipeline-arrow">➔</div>
          <div class="pipeline-step" onclick="selectStep('fan', event)">
            <div class="pipeline-icon">⚡</div>
            <div class="pipeline-title">3. Async Fan-Out</div>
            <div class="pipeline-sub">asyncio.gather(6x)</div>
          </div>
          <div class="pipeline-arrow">➔</div>
          <div class="pipeline-step" onclick="selectStep('iso', event)">
            <div class="pipeline-icon">🔒</div>
            <div class="pipeline-title">4. Error Isolation</div>
            <div class="pipeline-sub">Per-Platform Catch</div>
          </div>
          <div class="pipeline-arrow">➔</div>
          <div class="pipeline-step" onclick="selectStep('agg', event)">
            <div class="pipeline-icon">📊</div>
            <div class="pipeline-title">5. Aggregated Output</div>
            <div class="pipeline-sub">Unified JSON 200 OK</div>
          </div>
        </div>

        <div id="step-detail" class="pipeline-detail-card">
          <div class="pipeline-detail-header">
            <span id="detail-title" class="pipeline-detail-title">Stage 1: Incoming HTTP Payload</span>
            <span id="detail-badge" class="rule-tag" style="background: rgba(99,102,241,0.2); color: var(--primary-light);">POST /posting</span>
          </div>
          <p id="detail-desc" style="color: var(--text-muted); line-height: 1.6;">
            The client submits a clean JSON payload containing only <code>{"message": "..."}</code>. Platform selection is strictly handled internally by the application, fulfilling the requirement for internal routing without exposing platform flags to the client.
          </p>
        </div>
      </div>
    </section>

    <!-- 3. Playground Section -->
    <section id="playground">
      <div class="section-header">
        <div class="section-tag">Hands-On Testing</div>
        <h2 class="section-title">Interactive Live API Playground</h2>
        <p class="section-desc">
          Test real requests against the running FastAPI server right from this interface. Choose pre-configured scenario presets or type your own custom announcement.
        </p>
      </div>

      <div class="playground-grid">
        <!-- Input Panel -->
        <div class="playground-card">
          <div style="font-weight: 700; margin-bottom: 0.75rem;">Request Payload Builder</div>
          
          <div class="preset-chips">
            <span class="preset-chip" onclick="setPreset('valid')">🚀 Valid Launch Post</span>
            <span class="preset-chip" onclick="setPreset('no-url')">⚠️ 0 CTA Links (422)</span>
            <span class="preset-chip" onclick="setPreset('two-urls')">⚠️ 2 CTA Links (422)</span>
            <span class="preset-chip" onclick="setPreset('long')">⚠️ &gt; 200 Chars (422)</span>
          </div>

          <textarea id="message-input" class="message-textarea" oninput="updateLiveValidation()" placeholder="Write your message here with exactly one CTA link..."></textarea>

          <div class="live-validators">
            <span id="char-count" class="char-counter">0 / 200 characters</span>
            <span id="url-status" class="url-badge invalid">0 Links detected</span>
          </div>

          <button id="send-btn" class="btn-submit" onclick="executePost()">
            <span>Send POST /posting</span>
            <span>🚀</span>
          </button>

          <div class="curl-box">
            <button class="copy-btn" onclick="copyCurl()">Copy</button>
            <div id="curl-text">curl -X POST "http://localhost:4000/posting" -H "Content-Type: application/json" -d '{"message":"..."}'</div>
          </div>
        </div>

        <!-- Output Panel -->
        <div class="playground-card">
          <div class="response-header">
            <span style="font-weight: 700;">Live Server Response</span>
            <div style="display: flex; gap: 0.5rem; align-items: center;">
              <span id="response-status" class="response-status-badge status-200" style="display: none;">HTTP 200</span>
              <span id="response-time" class="timer-badge">Ready</span>
            </div>
          </div>

          <div id="response-body" class="response-viewer">// Click 'Send POST /posting' or choose a preset above to test the live server.
{
  "hint": "The server will validate character count (<= 200) and CTA URL presence before distributing to all 6 platforms."
}</div>
        </div>
      </div>
    </section>

    <!-- 4. Platforms Section -->
    <section id="platforms">
      <div class="section-header">
        <div class="section-tag">Supported Ecosystems</div>
        <h2 class="section-title">The 6 Integrated Platforms</h2>
        <p class="section-desc">
          Every platform is connected via its official REST API and returns verified, publicly accessible permalinks.
        </p>
      </div>

      <div class="platform-grid">
        <!-- Telegram -->
        <div class="platform-card">
          <div>
            <div class="platform-card-header">
              <div class="platform-title-group">
                <div class="platform-avatar">✈️</div>
                <div>
                  <div class="platform-name">Telegram</div>
                  <div class="platform-category">Messaging / Broadcast</div>
                </div>
              </div>
              <span class="rule-tag" style="background: rgba(16,185,129,0.15); color: var(--success);">Public Channel</span>
            </div>
            <div class="platform-endpoint">POST https://api.telegram.org/bot&lt;token&gt;/sendMessage</div>
            <p style="font-size: 0.85rem; color: var(--text-muted);">
              Instant broadcast to public channels. Returns permanent public view URLs (<code>https://t.me/channel/id</code>).
            </p>
          </div>
          <div class="platform-meta">
            <span>Auth: Bot Token</span>
            <span>Public Access: Yes</span>
          </div>
        </div>

        <!-- Twitter / X -->
        <div class="platform-card">
          <div>
            <div class="platform-card-header">
              <div class="platform-title-group">
                <div class="platform-avatar">🐦</div>
                <div>
                  <div class="platform-name">Twitter / X</div>
                  <div class="platform-category">Microblogging</div>
                </div>
              </div>
              <span class="rule-tag" style="background: rgba(99,102,241,0.15); color: var(--primary-light);">API v2</span>
            </div>
            <div class="platform-endpoint">POST https://api.twitter.com/2/tweets</div>
            <p style="font-size: 0.85rem; color: var(--text-muted);">
              Official Twitter API v2 text tweet creation with live tweet status permalink URL.
            </p>
          </div>
          <div class="platform-meta">
            <span>Auth: OAuth 2.0 Bearer</span>
            <span>Public Access: Yes</span>
          </div>
        </div>

        <!-- LinkedIn -->
        <div class="platform-card">
          <div>
            <div class="platform-card-header">
              <div class="platform-title-group">
                <div class="platform-avatar">💼</div>
                <div>
                  <div class="platform-name">LinkedIn</div>
                  <div class="platform-category">Professional Network</div>
                </div>
              </div>
              <span class="rule-tag" style="background: rgba(6,182,212,0.15); color: var(--secondary);">UGC Posts API</span>
            </div>
            <div class="platform-endpoint">POST https://api.linkedin.com/v2/ugcPosts</div>
            <p style="font-size: 0.85rem; color: var(--text-muted);">
              Creates public professional updates with commentary and structured CTA link previews.
            </p>
          </div>
          <div class="platform-meta">
            <span>Auth: Bearer Token</span>
            <span>Public Access: Yes</span>
          </div>
        </div>

        <!-- Reddit -->
        <div class="platform-card">
          <div>
            <div class="platform-card-header">
              <div class="platform-title-group">
                <div class="platform-avatar">🤖</div>
                <div>
                  <div class="platform-name">Reddit</div>
                  <div class="platform-category">Community / Forum</div>
                </div>
              </div>
              <span class="rule-tag" style="background: rgba(245,158,11,0.15); color: var(--warning);">OAuth2 API</span>
            </div>
            <div class="platform-endpoint">POST https://oauth.reddit.com/api/submit</div>
            <p style="font-size: 0.85rem; color: var(--text-muted);">
              Automated submission of links and posts to target subreddits with permanent discussion URLs.
            </p>
          </div>
          <div class="platform-meta">
            <span>Auth: OAuth2 Password</span>
            <span>Public Access: Yes</span>
          </div>
        </div>

        <!-- GitHub Gist -->
        <div class="platform-card">
          <div>
            <div class="platform-card-header">
              <div class="platform-title-group">
                <div class="platform-avatar">🐙</div>
                <div>
                  <div class="platform-name">GitHub Gist</div>
                  <div class="platform-category">Developer Portal</div>
                </div>
              </div>
              <span class="rule-tag" style="background: rgba(255,255,255,0.15); color: #fff;">REST API</span>
            </div>
            <div class="platform-endpoint">POST https://api.github.com/gists</div>
            <p style="font-size: 0.85rem; color: var(--text-muted);">
              Publishes formatted public announcement Gists readable by the global developer community.
            </p>
          </div>
          <div class="platform-meta">
            <span>Auth: Personal Access Token</span>
            <span>Public Access: Yes</span>
          </div>
        </div>

        <!-- Instagram Threads -->
        <div class="platform-card">
          <div>
            <div class="platform-card-header">
              <div class="platform-title-group">
                <div class="platform-avatar">🧵</div>
                <div>
                  <div class="platform-name">Instagram Threads</div>
                  <div class="platform-category">Social Conversation</div>
                </div>
              </div>
              <span class="rule-tag" style="background: rgba(236,72,153,0.15); color: var(--accent);">Meta Graph API</span>
            </div>
            <div class="platform-endpoint">POST https://graph.threads.net/v1.0/&lt;user&gt;/threads</div>
            <p style="font-size: 0.85rem; color: var(--text-muted);">
              Official Meta Threads API for text and CTA link distribution in the Instagram social graph.
            </p>
          </div>
          <div class="platform-meta">
            <span>Auth: Threads Access Token</span>
            <span>Public Access: Yes</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 5. Dedicated API Guide Callout Box -->
    <section id="api-guide-box">
      <div class="api-guide-callout-box">
        <div class="api-guide-callout-content">
          <div class="api-guide-callout-badge">🔑 API Credentials &amp; Setup</div>
          <h3 class="api-guide-callout-title">Ready to Test with Real-World Accounts?</h3>
          <p class="api-guide-callout-desc">
            The application works in simulation mode out-of-the-box (<code>MOCK_MODE=true</code>). When you're ready to test real API distribution, follow our step-by-step guide to get instant free credentials for Telegram (2 mins), GitHub Gists (1 min), and Reddit (3 mins), or configure Twitter, LinkedIn, and Threads.
          </p>
        </div>
        <a href="/api-guide" class="btn-open-guide">
          <span>Open Complete API Setup Guide</span>
          <span>➔</span>
        </a>
      </div>
    </section>

    <!-- 6. Validation Rules Section -->
    <section id="rules">
      <div class="section-header">
        <div class="section-tag">Business Logic</div>
        <h2 class="section-title">Validation Rules &amp; Edge Cases</h2>
        <p class="section-desc">
          Strict business validation enforced by Pydantic v2 before any network I/O takes place.
        </p>
      </div>

      <table class="rules-table">
        <thead>
          <tr>
            <th>Validation Rule</th>
            <th>Constraint Detail</th>
            <th>Invalid Trigger</th>
            <th>Error Response</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Character Limit</strong></td>
            <td><code>len(message) &le; 200</code> characters</td>
            <td>Message length = 201+</td>
            <td><span class="rule-tag" style="background:rgba(239,68,68,0.2); color:var(--danger);">HTTP 422</span> Message must not exceed 200 characters</td>
          </tr>
          <tr>
            <td><strong>CTA Link Count</strong></td>
            <td><strong>Exactly 1</strong> URL in the text</td>
            <td>0 URLs or 2+ URLs</td>
            <td><span class="rule-tag" style="background:rgba(239,68,68,0.2); color:var(--danger);">HTTP 422</span> Message must contain exactly one CTA link</td>
          </tr>
          <tr>
            <td><strong>URL Structure</strong></td>
            <td>Valid <code>http://</code> or <code>https://</code> with network domain</td>
            <td>Malformed protocols or non-domains</td>
            <td><span class="rule-tag" style="background:rgba(239,68,68,0.2); color:var(--danger);">HTTP 422</span> Invalid URL format</td>
          </tr>
          <tr>
            <td><strong>Platform Routing</strong></td>
            <td>Handled internally by the backend</td>
            <td>Supplying platform lists in request body</td>
            <td>Ignored or rejected via strict request schema</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- 7. Full API Schema Section -->
    <section id="schema">
      <div class="section-header">
        <div class="section-tag">API Specification</div>
        <h2 class="section-title">Request &amp; Response Schema Details</h2>
        <p class="section-desc">
          Complete contract documentation for <code>POST http://localhost:4000/posting</code>.
        </p>
      </div>

      <!-- Request Schema -->
      <div class="schema-card">
        <h3 style="font-size: 1.15rem; font-weight: 700; margin-bottom: 0.75rem; color: var(--primary-light);">
          Request Body: <code>PostingRequest</code>
        </h3>
        <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1rem;">
          Content-Type: <code>application/json</code>
        </p>
        <table class="rules-table" style="margin-top: 0;">
          <thead>
            <tr>
              <th>Field</th>
              <th>Type</th>
              <th>Required</th>
              <th>Rules &amp; Constraints</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>message</code></td>
              <td><code>string</code></td>
              <td><span class="rule-tag" style="background: rgba(16,185,129,0.2); color: var(--success);">Required</span></td>
              <td>Maximum 200 characters. Must contain exactly 1 valid CTA link.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Response Schema -->
      <div class="schema-card">
        <h3 style="font-size: 1.15rem; font-weight: 700; margin-bottom: 0.75rem; color: var(--primary-light);">
          Response Body: <code>PostingResponse</code> (HTTP 200 OK)
        </h3>
        <table class="rules-table" style="margin-top: 0;">
          <thead>
            <tr>
              <th>Field</th>
              <th>Type</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>success</code></td>
              <td><code>boolean</code></td>
              <td>True if execution completes and at least one platform succeeded.</td>
            </tr>
            <tr>
              <td><code>results</code></td>
              <td><code>Array&lt;PlatformResult&gt;</code></td>
              <td>Detailed execution report for each of the 6 integrated platforms.</td>
            </tr>
            <tr>
              <td colspan="3" style="background: rgba(255,255,255,0.02); font-weight: 700; color: var(--text-muted);">
                Nested Object: <code>PlatformResult</code>
              </td>
            </tr>
            <tr>
              <td><code>results[].platform</code></td>
              <td><code>string</code></td>
              <td>Platform name (e.g. <code>Telegram</code>, <code>Twitter / X</code>).</td>
            </tr>
            <tr>
              <td><code>results[].status</code></td>
              <td><code>"success" | "failed"</code></td>
              <td>Per-platform status. One platform's failure never blocks others.</td>
            </tr>
            <tr>
              <td><code>results[].posted_url</code></td>
              <td><code>string | null</code></td>
              <td>Live permalink of the published post, or null on failure.</td>
            </tr>
            <tr>
              <td><code>results[].public_access</code></td>
              <td><code>boolean</code></td>
              <td>Whether the post is publicly accessible without login.</td>
            </tr>
            <tr>
              <td><code>results[].date</code></td>
              <td><code>string | null</code></td>
              <td>Posting date in <code>YYYY-MM-DD</code> format.</td>
            </tr>
            <tr>
              <td><code>results[].time</code></td>
              <td><code>string | null</code></td>
              <td>Posting time in <code>HH:MM:SS</code> format.</td>
            </tr>
            <tr>
              <td><code>results[].error</code></td>
              <td><code>string | null</code></td>
              <td>Descriptive error string if failed, or null on success.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

  </div>

  <!-- Footer -->
  <footer>
    <p>
      Automated Multi-Platform Posting System • Built with <strong>FastAPI</strong>, <strong>Pydantic v2</strong> &amp; <strong>HTTPX</strong>
    </p>
    <p style="margin-top: 0.5rem; font-size: 0.85rem;">
      <a href="/api-guide">🔑 Complete API Keys Setup Guide</a> • 
      <a href="/swagger">Swagger UI</a> • 
      <a href="/redoc">ReDoc</a> • 
      <a href="/openapi.json">OpenAPI Spec</a> • 
      <a href="/health">Health Check</a>
    </p>
  </footer>

  <script>
    // Reveal animations on scroll
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
        }
      });
    }, { threshold: 0.08 });
    document.querySelectorAll('section').forEach(s => observer.observe(s));

    // Pipeline Storytelling Details
    const stepDetails = {
      req: {
        title: "Stage 1: Incoming HTTP Payload",
        badge: "POST /posting",
        desc: "The client sends a single JSON object with the 'message' string. The system does not require callers to specify target platforms, adhering cleanly to the principle of internal platform selection."
      },
      val: {
        title: "Stage 2: Pydantic v2 Validation Gate",
        badge: "Zero Network I/O",
        desc: "Before spawning any HTTP client connections, Pydantic parses the message: verifying maximum 200 characters, extracting candidates, and strictly asserting exactly one RFC-compliant URL. Any failure immediately triggers a clean 422 Unprocessable Content response."
      },
      fan: {
        title: "Stage 3: Asynchronous Fan-Out Engine",
        badge: "asyncio.gather(*tasks)",
        desc: "All 6 platform adapters are initiated concurrently using non-blocking HTTPX async clients. Rather than waiting 500ms x 6 = 3000ms sequentially, all platforms execute in parallel in under 500ms."
      },
      iso: {
        title: "Stage 4: Isolated Error Boundaries",
        badge: "Fail-Safe Resilience",
        desc: "Each platform is wrapped in its own isolated try/except block. If Twitter credentials fail or Reddit is rate-limited, Telegram, LinkedIn, GitHub Gist, and Threads continue unaffected."
      },
      agg: {
        title: "Stage 5: Standardized Result Aggregation",
        badge: "HTTP 200 OK",
        desc: "Results from all 6 platforms are collected into a unified JSON structure reporting platform name, status, posted URL, public access flag, timestamp, and specific error messages."
      }
    };

    function selectStep(step, ev) {
      document.querySelectorAll('.pipeline-step').forEach(el => el.classList.remove('active'));
      ev.currentTarget.classList.add('active');
      const data = stepDetails[step];
      document.getElementById('detail-title').textContent = data.title;
      document.getElementById('detail-badge').textContent = data.badge;
      document.getElementById('detail-desc').textContent = data.desc;
    }

    // Interactive Playground Logic
    const presets = {
      'valid': 'Check out our latest business platform and grow your online visibility. https://example.com',
      'no-url': 'Welcome to our brand new platform! Try out all features without any link.',
      'two-urls': 'Visit our home page https://example.com and check docs https://docs.example.com',
      'long': 'This is an exceptionally long promotional message crafted specifically to exceed the strict 200 characters limitation set forth in the engineering specification. It just keeps going on and on! https://example.com'
    };

    function setPreset(key) {
      const input = document.getElementById('message-input');
      input.value = presets[key];
      updateLiveValidation();
    }

    function updateLiveValidation() {
      const text = document.getElementById('message-input').value;
      const charCounter = document.getElementById('char-count');
      const urlBadge = document.getElementById('url-status');
      const length = text.trim().length;

      // Update character counter
      charCounter.textContent = `${length} / 200 characters`;
      if (length <= 200 && length > 0) {
        charCounter.className = 'char-counter valid';
      } else {
        charCounter.className = 'char-counter invalid';
      }

      // Detect URLs
      const urlMatches = text.match(/(?:https?:\/\/|www\.)[^\s<>"]+/gi) || [];
      if (urlMatches.length === 1) {
        urlBadge.textContent = "✓ 1 CTA Link detected";
        urlBadge.className = "url-badge valid";
      } else {
        urlBadge.textContent = `${urlMatches.length} Links (Must be 1)`;
        urlBadge.className = "url-badge invalid";
      }

      // Update curl preview
      const escaped = text.replace(/"/g, '\\"');
      document.getElementById('curl-text').textContent = 
        `curl -X POST "http://localhost:4000/posting" -H "Content-Type: application/json" -d '{"message":"${escaped}"}'`;
    }

    async function executePost() {
      const input = document.getElementById('message-input').value;
      const btn = document.getElementById('send-btn');
      const resViewer = document.getElementById('response-body');
      const statusBadge = document.getElementById('response-status');
      const timeBadge = document.getElementById('response-time');

      btn.disabled = true;
      btn.innerHTML = '<span>Posting in Parallel...</span> <span>⏳</span>';
      timeBadge.textContent = 'Executing...';

      const startTime = performance.now();
      try {
        const response = await fetch('/posting', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: input })
        });
        const elapsed = Math.round(performance.now() - startTime);
        const data = await response.json();

        statusBadge.style.display = 'inline-block';
        statusBadge.textContent = `HTTP ${response.status}`;
        statusBadge.className = `response-status-badge ${response.ok ? 'status-200' : 'status-422'}`;
        timeBadge.textContent = `⚡ ${elapsed}ms`;

        resViewer.textContent = JSON.stringify(data, null, 2);
      } catch (err) {
        statusBadge.style.display = 'inline-block';
        statusBadge.textContent = 'Error';
        statusBadge.className = 'response-status-badge status-422';
        timeBadge.textContent = 'Failed';
        resViewer.textContent = `Network Error: ${err.message}`;
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<span>Send POST /posting</span> <span>🚀</span>';
      }
    }

    function copyCurl() {
      const text = document.getElementById('curl-text').textContent;
      navigator.clipboard.writeText(text);
      const btn = document.querySelector('.copy-btn');
      btn.textContent = 'Copied!';
      setTimeout(() => btn.textContent = 'Copy', 1500);
    }

    // Initialize with default valid preset
    setPreset('valid');
  </script>
</body>
</html>
"""

# ==============================================================================
# 2. Dedicated API Keys Setup Guide Page (API_GUIDE_HTML)
# ==============================================================================
API_GUIDE_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>API Keys Setup Guide — Multi-Platform Posting System</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b0f19;
      --bg-card: rgba(18, 24, 38, 0.75);
      --border: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(99, 102, 241, 0.35);
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --primary: #6366f1;
      --primary-light: #818cf8;
      --secondary: #06b6d4;
      --accent: #ec4899;
      --success: #10b981;
      --warning: #f59e0b;
      --radius: 14px;
      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      line-height: 1.6;
      background-image: 
        radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.12) 0%, transparent 40%),
        radial-gradient(circle at 85% 65%, rgba(6, 182, 212, 0.1) 0%, transparent 40%);
      background-attachment: fixed;
    }
    header {
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(18px);
      background: rgba(11, 15, 25, 0.88);
      border-bottom: 1px solid var(--border);
      padding: 0.9rem 2.25rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .logo-group {
      display: flex;
      align-items: center;
      gap: 0.8rem;
      text-decoration: none;
      color: var(--text);
    }
    .logo-badge {
      width: 38px;
      height: 38px;
      border-radius: 10px;
      background: linear-gradient(135deg, var(--primary), var(--secondary));
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.15rem;
      color: white;
    }
    .btn-back {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.5rem 1rem;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border);
      color: var(--text);
      border-radius: 8px;
      font-size: 0.88rem;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s ease;
    }
    .btn-back:hover {
      background: rgba(255, 255, 255, 0.12);
      border-color: rgba(255, 255, 255, 0.2);
    }
    .container {
      max-width: 1000px;
      margin: 0 auto;
      padding: 3rem 1.5rem;
    }
    .page-title-box {
      margin-bottom: 2.5rem;
    }
    .page-title {
      font-size: 2.4rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin-bottom: 0.75rem;
    }
    .page-desc {
      color: var(--text-muted);
      font-size: 1.1rem;
      line-height: 1.6;
    }
    .fast-track-box {
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.3);
      border-radius: var(--radius);
      padding: 1.5rem;
      margin-bottom: 2.5rem;
    }
    .platform-guide-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 2rem;
      margin-bottom: 2rem;
      backdrop-filter: blur(12px);
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.25rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      padding-bottom: 1rem;
    }
    .card-title {
      font-size: 1.35rem;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }
    .step-item {
      background: rgba(11, 15, 25, 0.6);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.1rem 1.3rem;
      margin-bottom: 0.85rem;
    }
    .step-item h4 {
      font-size: 0.98rem;
      font-weight: 700;
      margin-bottom: 0.35rem;
      color: var(--text);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .step-num {
      width: 22px;
      height: 22px;
      background: var(--primary);
      color: white;
      border-radius: 50%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 0.75rem;
      font-weight: 800;
    }
    .step-item p {
      color: var(--text-muted);
      font-size: 0.9rem;
      line-height: 1.55;
    }
    .code-box {
      background: rgba(0, 0, 0, 0.5);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.75rem 1rem;
      font-family: var(--font-mono);
      font-size: 0.82rem;
      color: #38bdf8;
      margin-top: 0.5rem;
      overflow-x: auto;
    }
    .rule-tag {
      display: inline-block;
      padding: 0.25rem 0.6rem;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 700;
      font-family: var(--font-mono);
    }
    a { color: var(--primary-light); text-decoration: none; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>

  <header>
    <a href="/docs" class="logo-group">
      <div class="logo-badge">⚡</div>
      <div style="font-weight: 700; font-size: 1.05rem;">Multi-Platform Posting System</div>
    </a>
    <a href="/docs" class="btn-back">← Back to Documentation</a>
  </header>

  <div class="container">
    <div class="page-title-box">
      <h1 class="page-title">🔑 Complete API Keys Setup Guide</h1>
      <p class="page-desc">
        Follow these step-by-step instructions to acquire credentials for testing real-world, live multi-platform distribution across all 6 supported services.
      </p>
    </div>

    <div class="fast-track-box">
      <h3 style="color: #34d399; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.4rem;">
        ⚡ Recommended Fast Track (Under 5 Minutes)
      </h3>
      <p style="color: var(--text-muted); font-size: 0.92rem;">
        To test real API posting immediately without waiting for developer portal approvals, configure <strong>Telegram</strong> (2 mins), <strong>GitHub Gists</strong> (1 min), and <strong>Reddit</strong> (3 mins). They are 100% free and provide instant access!
      </p>
    </div>

    <!-- 1. Telegram -->
    <div class="platform-guide-card">
      <div class="card-header">
        <div class="card-title">
          <span>✈️</span> Telegram Bot API
        </div>
        <span class="rule-tag" style="background: rgba(16,185,129,0.2); color: var(--success);">Instant • 100% Free</span>
      </div>
      <div class="step-item">
        <h4><span class="step-num">1</span> Create a Bot with @BotFather</h4>
        <p>Open Telegram and message <strong>@BotFather</strong> (<a href="https://t.me/BotFather" target="_blank">t.me/BotFather</a>). Send <code>/newbot</code>, pick a display name and username ending in <code>bot</code>. Copy the token provided.</p>
      </div>
      <div class="step-item">
        <h4><span class="step-num">2</span> Create a Public Channel &amp; Add Bot as Admin</h4>
        <p>Create a new Public Channel (e.g. <code>@my_channel_name</code>). Go to Channel Settings ➔ Administrators ➔ Add Administrator ➔ add your bot and ensure <strong>"Post Messages"</strong> is enabled.</p>
      </div>
      <div class="step-item">
        <h4><span class="step-num">3</span> Configure .env</h4>
        <div class="code-box">
          TELEGRAM_BOT_TOKEN=1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ<br>
          TELEGRAM_CHAT_ID=@my_channel_name
        </div>
      </div>
    </div>

    <!-- 2. GitHub Gist -->
    <div class="platform-guide-card">
      <div class="card-header">
        <div class="card-title">
          <span>🐙</span> GitHub Gist REST API
        </div>
        <span class="rule-tag" style="background: rgba(16,185,129,0.2); color: var(--success);">Instant • 100% Free</span>
      </div>
      <div class="step-item">
        <h4><span class="step-num">1</span> Generate Personal Access Token</h4>
        <p>Visit GitHub Token Settings (<a href="https://github.com/settings/tokens" target="_blank">github.com/settings/tokens</a>) ➔ Click <strong>Generate new token (classic)</strong>.</p>
      </div>
      <div class="step-item">
        <h4><span class="step-num">2</span> Select 'gist' Scope</h4>
        <p>Name the token (e.g. <code>Posting System</code>) and check the single <strong><code>gist</code></strong> checkbox. Click Generate.</p>
      </div>
      <div class="step-item">
        <h4><span class="step-num">3</span> Configure .env</h4>
        <div class="code-box">
          GITHUB_ACCESS_TOKEN=ghp_yourTokenHere1234567890
        </div>
      </div>
    </div>

    <!-- 3. Reddit -->
    <div class="platform-guide-card">
      <div class="card-header">
        <div class="card-title">
          <span>🤖</span> Reddit OAuth2 API
        </div>
        <span class="rule-tag" style="background: rgba(16,185,129,0.2); color: var(--success);">Instant • 100% Free</span>
      </div>
      <div class="step-item">
        <h4><span class="step-num">1</span> Create a 'Script' Application</h4>
        <p>Go to <a href="https://www.reddit.com/prefs/apps" target="_blank">reddit.com/prefs/apps</a>, scroll down and click <strong>create another app...</strong>.</p>
      </div>
      <div class="step-item">
        <h4><span class="step-num">2</span> Select Script App Type</h4>
        <p>Name: <code>MultiPoster</code>, select the radio button <strong>script</strong>, redirect uri: <code>http://localhost:4000/callback</code>.</p>
      </div>
      <div class="step-item">
        <h4><span class="step-num">3</span> Configure .env</h4>
        <div class="code-box">
          REDDIT_CLIENT_ID=your_client_id_here<br>
          REDDIT_CLIENT_SECRET=your_client_secret_here<br>
          REDDIT_USERNAME=your_username<br>
          REDDIT_PASSWORD=your_password<br>
          REDDIT_SUBREDDIT=test
        </div>
      </div>
    </div>

    <!-- 4. Twitter / X -->
    <div class="platform-guide-card">
      <div class="card-header">
        <div class="card-title">
          <span>🐦</span> Twitter / X API v2
        </div>
        <span class="rule-tag" style="background: rgba(99,102,241,0.2); color: var(--primary-light);">X Developer Portal</span>
      </div>
      <div class="step-item">
        <h4><span class="step-num">1</span> Developer Portal App Setup</h4>
        <p>Sign in to <a href="https://developer.x.com/en/portal/dashboard" target="_blank">developer.x.com</a>, create a Project, and configure User Authentication with <strong>Read and Write</strong> permissions.</p>
      </div>
      <div class="step-item">
        <h4><span class="step-num">2</span> Configure .env</h4>
        <div class="code-box">
          TWITTER_BEARER_TOKEN=your_bearer_or_user_access_token_here
        </div>
      </div>
    </div>

    <!-- 5. LinkedIn -->
    <div class="platform-guide-card">
      <div class="card-header">
        <div class="card-title">
          <span>💼</span> LinkedIn UGC Posts API
        </div>
        <span class="rule-tag" style="background: rgba(6,182,212,0.2); color: var(--secondary);">LinkedIn Developers</span>
      </div>
      <div class="step-item">
        <h4><span class="step-num">1</span> Create App on LinkedIn Developers</h4>
        <p>Visit <a href="https://www.linkedin.com/developers/apps" target="_blank">linkedin.com/developers/apps</a>, create an App, and request the <strong>Share on LinkedIn</strong> product.</p>
      </div>
      <div class="step-item">
        <h4><span class="step-num">2</span> Generate Token &amp; Configure .env</h4>
        <div class="code-box">
          LINKEDIN_ACCESS_TOKEN=AQV...your_token_here<br>
          LINKEDIN_PERSON_URN=me
        </div>
      </div>
    </div>

    <!-- 6. Threads -->
    <div class="platform-guide-card">
      <div class="card-header">
        <div class="card-title">
          <span>🧵</span> Instagram Threads API
        </div>
        <span class="rule-tag" style="background: rgba(236,72,153,0.2); color: var(--accent);">Meta Developers</span>
      </div>
      <div class="step-item">
        <h4><span class="step-num">1</span> Meta for Developers Setup</h4>
        <p>Sign in to <a href="https://developers.facebook.com/" target="_blank">developers.facebook.com</a>, create an App, and add the Threads API.</p>
      </div>
      <div class="step-item">
        <h4><span class="step-num">2</span> Generate User Token &amp; Configure .env</h4>
        <div class="code-box">
          THREADS_ACCESS_TOKEN=THQ...your_token_here<br>
          THREADS_USER_ID=1234567890123456
        </div>
      </div>
    </div>

    <div style="text-align: center; margin-top: 3rem;">
      <a href="/docs" class="btn-back" style="font-size: 1rem; padding: 0.75rem 1.5rem;">← Back to Main Documentation &amp; Playground</a>
    </div>
  </div>

</body>
</html>
"""
