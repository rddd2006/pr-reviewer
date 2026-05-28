# Extension Comparison & Quick Start

## 📊 Extension Options

| Feature | Chrome Ext | GitHub App | VS Code Ext |
|---------|-----------|-----------|-----------|
| **Setup Time** | 5 min | 20 min | 10 min |
| **Use Case** | Any GitHub PR | Automatic PR review | Local development |
| **Requires Server** | Yes | Yes | Yes |
| **Browser Support** | Chrome, Edge | GitHub only | VS Code only |
| **Auto-review** | ❌ Manual | ✅ Yes | ❌ Manual |
| **Inline Comments** | ❌ | ✅ | ✅ |
| **Cost** | Low | Low | Low |
| **Privacy** | Moderate | High (GitHub-only) | Highest (local) |

---

## 🚀 Quick Start (Choose One)

### Option 1: Chrome Extension (Easiest)

**⏱️ 5 minutes**

```bash
# 1. Start API server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python api_server.py

# 2. Load extension
# - Go to chrome://extensions
# - Turn on "Developer mode"
# - Click "Load unpacked"
# - Select extensions/chrome/
# - Configure API URL: http://localhost:8000

# 3. Use it
# - Go to any GitHub PR
# - Click Diff Reviewer extension
# - Select "review" and click "Review Current PR"
```

**For Production:**
```bash
# Deploy API server (Heroku, Docker, AWS Lambda, etc.)
# Update extension with production API URL
# Publish to Chrome Web Store
```

---

### Option 2: GitHub App (Best for Teams)

**⏱️ 20 minutes**

```bash
# 1. Create GitHub App
# - Go to https://github.com/settings/apps
# - "New GitHub App"
# - Set webhook URL to your server
# - Generate webhook secret

# 2. Deploy webhook handler
docker build -t diff-reviewer .
docker run -p 8000:8000 \
  -e GITHUB_APP_ID=your_id \
  -e GITHUB_WEBHOOK_SECRET=your_secret \
  -e OPENAI_API_KEY=your_key \
  diff-reviewer

# 3. Install on repository
# - GitHub App page → Install
# - Select repositories

# 4. Done!
# PRs are automatically reviewed
```

**Use case:** Team workflows, automatic reviews, CI/CD integration

---

### Option 3: VS Code Extension (For Developers)

**⏱️ 10 minutes**

```bash
# 1. Start API server (same as Chrome)
python api_server.py

# 2. Develop extension
cd extensions/vscode
npm install
npm run compile

# 3. Debug in VS Code
# - Press F5 to open extension in new window
# - Open diff file
# - Run: Diff Reviewer: Review Diff

# 4. Configure
# - Settings → Search "Diff Reviewer"
# - Set API URL to http://localhost:8000
```

**Use case:** Local development, custom workflows, integrations

---

## 📦 Deployment Options

### Self-Hosted (Recommended for Privacy)

```bash
# Option A: Docker Compose (Simplest)
docker-compose up -d

# Option B: Heroku
git push heroku main

# Option C: DigitalOcean App Platform
# Connect GitHub repo, deploy

# Option D: AWS Lambda
# Use Zappa or Serverless Framework
```

### SaaS (Coming Soon)

Host API on our servers (will provide)

---

## 🔑 Environment Setup

1. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Add your API keys:**
   ```env
   # Choose one LLM provider
   OPENAI_API_KEY=sk-your-key
   # OR
   GEMINI_API_KEY=your-key
   
   # For GitHub App only
   GITHUB_APP_ID=12345
   GITHUB_WEBHOOK_SECRET=whsec_...
   ```

3. **Start API server:**
   ```bash
   python api_server.py
   ```

---

## ✅ Verification Checklist

- [ ] API server running: `curl http://localhost:8000/health`
- [ ] Environment variables set: `echo $OPENAI_API_KEY`
- [ ] For Chrome: Extension loaded and API URL configured
- [ ] For GitHub App: Webhook events showing in deliveries
- [ ] For VS Code: Extension showing in extensions list

---

## 🆘 Troubleshooting

**Chrome Extension not working?**
```bash
# Check API server
curl http://localhost:8000/health

# Check browser console
# Right-click extension → Inspect popup
# Look for error messages
```

**GitHub webhook not triggering?**
```bash
# Check GitHub settings
# App → Advanced → Recent Deliveries
# Look for error messages in red

# Test webhook manually
curl -X POST http://your-server.com/webhook/github \
  -H "Content-Type: application/json" \
  -d '{"zen":"test"}'
```

**API server timeout?**
```bash
# Increase timeout
export LLM_TIMEOUT_SECONDS=180

# Check logs
docker-compose logs -f api
```

---

## 🔒 Security Notes

- **API Keys**: Never commit `.env` file
- **Webhooks**: Always verify signatures (done automatically)
- **CORS**: Restrict to known domains in production
- **Rate Limiting**: Implement on production server
- **Authentication**: Use API keys or OAuth for teams

---

## 📚 Full Documentation

- [Extension Setup Guide](EXTENSION_SETUP.md)
- [GitHub App Details](extensions/github-app/README.md)
- [VS Code Extension](extensions/vscode/README.md)
- [API Server Docs](api_server.py)

---

## 🤝 Getting Help

- 📖 Check documentation above
- 🐛 Search existing issues
- 💬 Open a new issue with:
  - Extension type (Chrome/GitHub App/VS Code)
  - Steps to reproduce
  - Error messages from console/logs
  - Environment (Windows/Mac/Linux)

---

## 📝 Next Steps

1. Choose your extension type
2. Follow the quick start above
3. Test with a sample diff or PR
4. Deploy to production (optional)
5. Enjoy AI-powered code reviews! 🎉

---

## 🎯 Roadmap

- [ ] VS Code marketplace publication
- [ ] Chrome Web Store publication  
- [ ] GitHub Marketplace app
- [ ] Firefox extension
- [ ] Safari extension
- [ ] Automated GitHub Actions integration
- [ ] Custom model support (Llama, Mistral, etc.)
- [ ] Code review caching and analytics

---

**Questions?** Open an issue or start a discussion!
