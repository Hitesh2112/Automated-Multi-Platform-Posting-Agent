# Comprehensive Guide: Obtaining Real API Keys for Live Multi-Platform Testing

This document provides step-by-step instructions for acquiring real API credentials for each supported platform so you can test live, production posting with real accounts.

---

## Quick Reference & Setup Difficulty

| Platform | Setup Time | Difficulty | Cost | Immediate Approval? |
|---|---|---|---|---|
| **1. Telegram** | 2 minutes | Very Easy | 100% Free | **Instant** (No review needed) |
| **2. GitHub Gist** | 1 minute | Very Easy | 100% Free | **Instant** (Existing GitHub account) |
| **3. Reddit** | 3 minutes | Easy | 100% Free | **Instant** (Script application) |
| **4. Twitter / X** | 5-10 minutes | Moderate | Free tier / Paid | Developer Portal sign-up |
| **5. LinkedIn** | 5-10 minutes | Moderate | 100% Free | Developer Portal app creation |
| **6. Instagram Threads** | 5-10 minutes | Moderate | 100% Free | Meta Developer Portal |

> [!TIP]
> **Recommended Fast Track (Under 5 Minutes)**:
> If you want to test live real-world posting immediately without waiting for complex developer portal reviews, configure **Telegram**, **GitHub**, and **Reddit** first. They are instant, free, and require zero external review!

---

## 1. Telegram Bot API (Instant Setup — ~2 Minutes)

Telegram allows you to post directly to a public channel or group via a Telegram Bot.

### Steps to get credentials:

1. **Open Telegram** and search for the official account **`@BotFather`** (or go to [https://t.me/BotFather](https://t.me/BotFather)).
2. Send the command:
   ```text
   /newbot
   ```
3. Follow the prompts:
   - Enter a display name for your bot (e.g. `MyPostingBot`).
   - Enter a unique username ending in `bot` (e.g. `myposting_test_bot`).
4. `@BotFather` will reply with your **Bot Token**. It looks like:
   ```text
   1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ123456789
   ```
5. **Create a Public Channel**:
   - In Telegram, click **New Channel** $\to$ name it (e.g. `Test Announcements`).
   - Choose **Public Channel** and choose a public link username (e.g. `t.me/my_test_channel_123`).
6. **Add Bot as Administrator**:
   - Open your Channel Info $\to$ **Administrators** $\to$ **Add Administrator**.
   - Search for your bot username (`@myposting_test_bot`) and add it.
   - Ensure the permission **"Post Messages"** is enabled.
7. **Configure `.env`**:
   ```env
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ123456789
   TELEGRAM_CHAT_ID=@my_test_channel_123
   ```

*Public posts will appear live at `https://t.me/my_test_channel_123/<message_id>`.*

---

## 2. GitHub Gist API (Instant Setup — ~1 Minute)

Publishing public announcement Gists using your GitHub personal access token.

### Steps to get credentials:

1. Sign in to your [GitHub Account](https://github.com/).
2. Navigate to **Settings** $\to$ **Developer settings** $\to$ **Personal access tokens** $\to$ **Tokens (classic)** (or direct link: [https://github.com/settings/tokens](https://github.com/settings/tokens)).
3. Click **Generate new token** $\to$ **Generate new token (classic)**.
4. Fill in:
   - **Note**: `Multi-Platform Posting Test`
   - **Expiration**: Select `30 days` (or your preference).
   - **Select scopes**: Check the box for **`gist`** (Create gists).
5. Scroll down and click **Generate token**.
6. Copy the generated token (`ghp_...`).
7. **Configure `.env`**:
   ```env
   GITHUB_ACCESS_TOKEN=ghp_yourGeneratedTokenHere1234567890
   ```

*Public posts will appear live at `https://gist.github.com/<your-username>/<gist-id>`.*

---

## 3. Reddit OAuth2 API (Instant Setup — ~3 Minutes)

Submit posts to any subreddit (such as `r/test` or your own profile/subreddit) using a personal script app.

### Steps to get credentials:

1. Sign in to [Reddit](https://www.reddit.com/).
2. Navigate to Reddit's App Preferences: [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps).
3. Scroll to the bottom and click **create another app...** (or **create app...**).
4. Fill in:
   - **name**: `MultiPlatformPoster`
   - **App type**: Select the radio button **`script`** *(Important: Must be `script` for password authentication grant).*
   - **description**: Optional.
   - **about url**: Leave blank or enter `https://example.com`.
   - **redirect uri**: Enter `http://localhost:4000/callback` (or `http://localhost:8080`).
5. Click **create app**.
6. Retrieve your credentials:
   - **Client ID**: The string displayed immediately beneath **"personal use script"** (e.g. `k8F_abC123DeFg`).
   - **Client Secret**: The string labeled **secret** (e.g. `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5`).
7. **Configure `.env`**:
   ```env
   REDDIT_CLIENT_ID=k8F_abC123DeFg
   REDDIT_CLIENT_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5
   REDDIT_USERNAME=your_reddit_username
   REDDIT_PASSWORD=your_reddit_password
   REDDIT_SUBREDDIT=test
   ```
   *(Note: `r/test` is Reddit's official sandbox community for testing bot submissions).*

*Public posts will appear live at `https://www.reddit.com/r/test/comments/...`.*

---

## 4. Twitter / X API v2 (Developer Portal — ~5-10 Minutes)

Publish tweets to Twitter / X using the official API v2.

### Steps to get credentials:

1. Sign in to the [X Developer Portal](https://developer.x.com/en/portal/dashboard).
2. If you don't have a developer project, click **Create Project**, assign a name, use case (e.g. "Making a bot"), and description.
3. In your App settings:
   - Navigate to **Settings** $\to$ **User authentication settings** $\to$ click **Set up**.
   - **App permissions**: Select **Read and write**.
   - **Type of App**: Select **Web App, Automated App or Bot**.
   - **Callback URI / Redirect URL**: Enter `http://localhost:4000/callback`.
   - **Website URL**: Enter `https://example.com`.
   - Click **Save**.
4. Go to the **Keys and Tokens** tab:
   - Under **OAuth 2.0 Client ID and Client Secret**, click **Generate** and store them.
   - Under **Authentication Tokens**, generate your **User Access Token and Secret** (ensuring permissions are Read and Write), or generate a **Bearer Token**.
5. **Configure `.env`**:
   ```env
   TWITTER_BEARER_TOKEN=your_bearer_token_or_access_token_here
   ```

*Public posts will appear live at `https://x.com/your_username/status/<tweet_id>`.*

---

## 5. LinkedIn UGC Posts API (~5-10 Minutes)

Share public posts to your personal LinkedIn profile or company page.

### Steps to get credentials:

1. Go to the [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps).
2. Click **Create app**:
   - **App name**: `Multi-Platform Poster`
   - **LinkedIn Page**: Link to a LinkedIn Company page (or create a quick test page).
   - Upload any image for the app logo.
   - Click **Create app**.
3. In the **Products** tab:
   - Select **Share on LinkedIn** and click **Request access**.
   - (Optional) Select **Sign In with LinkedIn using OpenID Connect** for user info.
4. In the **Auth** tab:
   - Use LinkedIn's **OAuth 2.0 tools** or token generator to generate an Access Token with the `w_member_social` permission.
5. Identify your Person URN:
   - You can use `me` as the identifier, or query `https://api.linkedin.com/v2/userinfo` with your token to see your `sub` ID (e.g. `urn:li:person:abcdef123`).
6. **Configure `.env`**:
   ```env
   LINKEDIN_ACCESS_TOKEN=AQV...your_access_token...
   LINKEDIN_PERSON_URN=me
   ```

*Public posts will appear live at `https://www.linkedin.com/feed/update/urn:li:ugcPost:<id>`.*

---

## 6. Meta Threads / Instagram API (~5-10 Minutes)

Publish text conversation posts and links to Meta Threads (Instagram's text-based platform companion).

### Steps to get credentials:

1. Sign in to the [Meta for Developers Portal](https://developers.facebook.com/).
2. Click **My Apps** $\to$ **Create App**.
3. Select **Other** as the use case $\to$ choose app type (e.g. **Business** or **None**).
4. In the App Dashboard, locate **Threads API** and click **Set Up**.
5. Add a test user or your own Instagram/Threads account in **Roles** $\to$ **Test Users** (or App Roles).
6. Under **Threads API** $\to$ **API Explorer / Token Generator**, generate a User Access Token with the following permissions:
   - `threads_basic`
   - `threads_content_publish`
7. Retrieve your Threads User ID by querying `https://graph.threads.net/v1.0/me?access_token=<YOUR_TOKEN>`.
8. **Configure `.env`**:
   ```env
   THREADS_ACCESS_TOKEN=THQ...your_token_here...
   THREADS_USER_ID=1234567890123456
   ```

*Public posts will appear live at `https://www.threads.net/@your_username/post/<thread_id>`.*

---

## Testing Real Posting End-to-End

Once you have filled in credentials in your `.env` file for any or all of the platforms above:

### Step 1: Ensure `MOCK_MODE=false` in `.env`
```env
MOCK_MODE=false
```

### Step 2: Start the Server
```bash
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 4000
```

### Step 3: Trigger a Real Post
Run this curl command in your terminal:

```bash
curl -X POST "http://localhost:4000/posting" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Testing automated multi-platform posting live! Check it out: https://example.com"
     }'
```

### Step 4: Inspect the Response
You will receive an immediate response showing which platforms published live and their public URLs:
```json
{
  "success": true,
  "results": [
    {
      "platform": "Telegram",
      "status": "success",
      "posted_url": "https://t.me/my_test_channel_123/12",
      "public_access": true,
      "date": "2026-11-20",
      "time": "19:05:12",
      "error": null
    },
    {
      "platform": "GitHub Gist",
      "status": "success",
      "posted_url": "https://gist.github.com/myusername/a1b2c3d4e5f6g7h8",
      "public_access": true,
      "date": "2026-11-20",
      "time": "19:05:12",
      "error": null
    },
    {
      "platform": "Twitter / X",
      "status": "failed",
      "posted_url": null,
      "public_access": false,
      "date": null,
      "time": null,
      "error": "Authentication failed: Missing API credentials"
    }
  ]
}
```

Open the returned `posted_url` in your browser to verify the published content live!

---

## Troubleshooting Common API Errors

| Error Message / HTTP Status | Cause | Resolution |
|---|---|---|
| `Authentication failed: Missing API credentials` | Variable is empty in `.env` | Add the required keys to `.env` and restart the server. |
| `HTTP 401 Unauthorized` | Token is mistyped, expired, or revoked | Re-generate the token from the platform's developer dashboard. |
| `HTTP 403 Forbidden` | Token lacks sufficient permissions/scopes | Check that write permissions (`w_member_social`, `gist`, `threads_content_publish`, `tweet.write`) are granted. |
| `HTTP 429 Too Many Requests` | Platform rate limit reached | Wait 60 seconds before sending another post. |
| `Telegram API error: chat not found` | Bot is not in the channel or chat ID is wrong | Ensure the bot is added as an **Administrator** with "Post Messages" permission. |
