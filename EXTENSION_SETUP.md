# Extension Setup & Deployment Guide

## Overview

Diff Reviewer can be deployed as:
1. **Chrome Extension** - For reviewing any code on GitHub
2. **GitHub App** - For automatic PR reviews on GitHub
3. **VS Code Extension** - (Coming soon)

---

## Chrome Extension Setup

### Development Setup

1. **Prepare the API Server**:
```bash
# Install dependencies
pip install -r requirements.txt
pip install fastapi uvicorn

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Start the API server
python api_server.py
```

The API will be available at `http://localhost:8000`

2. **Load the Extension**:
   - Open `chrome://extensions`
   - Enable "Developer mode" (top right)
   - Click "Load unpacked"
   - Select the `extensions/chrome` folder

3. **Configure the Extension**:
   - Click the extension icon
   - Enter API URL: `http://localhost:8000`
   - Enter API Key (if required)
   - Click "Save Settings"

### Production Deployment

1. **Deploy API Server**:

**Option A: Heroku**
```bash
heroku create your-app-name
heroku config:set LLM_PROVIDER=openai
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

**Option B: Docker**
```bash
docker build -t diff-reviewer .
docker run -p 8000:8000 \
  -e LLM_PROVIDER=openai \
  -e OPENAI_API_KEY=your_key \
  diff-reviewer
```

**Option C: AWS Lambda**
```bash
# Use Zappa or Serverless framework
serverless deploy
```

2. **Update Extension**:
   - Open `extensions/chrome/manifest.json`
   - Update `host_permissions` with your API server URL
   - Rebuild and upload to Chrome Web Store

### Publishing to Chrome Web Store

1. Create a developer account on Chrome Web Store
2. Zip the extension: `zip -r diff-reviewer.zip extensions/chrome/`
3. Upload to https://chrome.google.com/webstore/devconsole
4. Fill in details and submit for review

---

## GitHub App Setup

### Prerequisites

- A GitHub account
- A public server (Heroku, AWS, DigitalOcean, etc.)
- The Diff Reviewer API running

### Setup Steps

1. **Create GitHub App** (detailed instructions in `extensions/github-app/README.md`)

2. **Deploy Webhook Handler**:

```bash
# Add webhook handler to your API server
cp extensions/github-app/webhook.py src/extensions/

# Update api_server.py to include webhook router
# (See implementation details below)

# Deploy server
```

3. **Configure Environment**:
```bash
export GITHUB_APP_ID=your_app_id
export GITHUB_PRIVATE_KEY=your_private_key
export GITHUB_WEBHOOK_SECRET=your_webhook_secret
```

4. **Test the Setup**:
```bash
curl -X POST http://your-server.com/webhook/github \
  -H "X-GitHub-Event: ping" \
  -d '{}'
```

---

## API Server Details

### Start the Server

**Development**:
```bash
python api_server.py
```

**Production**:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 api_server:app
```

### API Endpoints

#### POST /review
Review a diff

```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{
    "diff": "--- a/file.py\n+++ b/file.py\n...",
    "command": "review",
    "format": "text"
  }'
```

#### POST /batch-review
Review multiple diffs

```bash
curl -X POST http://localhost:8000/batch-review \
  -H "Content-Type: application/json" \
  -d '[
    {"diff": "...", "command": "review"},
    {"diff": "...", "command": "ask", "request": "Is this secure?"}
  ]'
```

#### GET /config
Get available commands and settings

#### GET /health
Health check

---

## Extension Architecture

### Chrome Extension

```
extensions/chrome/
├── manifest.json       # Extension configuration
├── popup.html          # UI for extension popup
├── popup.js            # Logic for popup
├── popup.css           # Styling
├── content.js          # GitHub page integration
├── background.js       # Service worker
└── images/             # Icons
```

### GitHub App

```
extensions/github-app/
├── app-manifest.json   # GitHub App configuration
├── webhook.py          # Webhook handler
└── README.md           # Setup instructions
```

---

## Environment Variables

### API Server

```bash
# LLM Configuration
LLM_PROVIDER=openai              # or gemini
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-pro

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
ENV=production

# LLM Settings
MAX_TOKENS=2000
LLM_TIMEOUT_SECONDS=120
ENABLE_COMPRESSION=true
LOG_LEVEL=INFO
```

### GitHub App

```bash
GITHUB_APP_ID=123456
GITHUB_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----\n...
GITHUB_WEBHOOK_SECRET=whsec_...
```

---

## Troubleshooting

### Chrome Extension Issues

**Issue**: "Extension not loading"
- Check Chrome version (Manifest V3 requires Chrome 88+)
- Clear cache and reload extension
- Check manifest.json for syntax errors

**Issue**: "API connection failed"
- Verify API server is running: `curl http://localhost:8000/health`
- Check CORS settings in API server
- Check browser console for specific errors

**Issue**: "Can't extract GitHub diff"
- Ensure you're on a PR page (not issue page)
- Check content script is loaded (should see message in browser console)
- Try refreshing the page

### GitHub App Issues

**Issue**: "Webhook not triggering"
- Check webhook secret matches in GitHub settings
- Verify server is publicly accessible
- Check GitHub App Advanced → Deliveries for error details

**Issue**: "Permission denied"
- Verify app has required permissions in settings
- Reinstall app on repository
- Check private key is correctly set

---

## Security Considerations

1. **API Keys**: Never commit `.env` files
2. **CORS**: Restrict to specific domains in production
3. **Rate Limiting**: Implement rate limits on API endpoints
4. **Authentication**: Consider API key validation for production
5. **Webhooks**: Always verify webhook signatures

---

## Support & Contributing

For issues, questions, or contributions, visit:
https://github.com/yourusername/diff-reviewer

---

## Next Steps

1. ✅ Set up API server
2. ✅ Load Chrome extension in development
3. ✅ Test with a local diff
4. ⏭️ Deploy API to production
5. ⏭️ Publish Chrome extension to Web Store
6. ⏭️ Create GitHub App
7. ⏭️ Install on your repository
