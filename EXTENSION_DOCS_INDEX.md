# 📖 Extension Documentation Index

## 🚀 **Start Here**

- **[EXTENSIONS_QUICK_START.md](EXTENSIONS_QUICK_START.md)** - 2-minute overview and quick start
- **[EXTENSION_IMPLEMENTATION_SUMMARY.md](EXTENSION_IMPLEMENTATION_SUMMARY.md)** - Complete implementation details

---

## 🎯 Choose Your Extension Type

### Chrome Extension (Easiest)
- **⏱️ Setup Time:** 5 minutes
- **📍 Use:** Review any GitHub PR in your browser
- **📖 Guide:** [extensions/chrome/INSTALL_GUIDE.md](extensions/chrome/INSTALL_GUIDE.md)
- **👥 Best For:** Individual developers, quick reviews
- **🔧 Files:**
  - [manifest.json](extensions/chrome/manifest.json) - Extension config
  - [popup.html](extensions/chrome/popup.html) - User interface
  - [content.js](extensions/chrome/content.js) - GitHub integration

### GitHub App (Best for Teams)
- **⏱️ Setup Time:** 20 minutes
- **📍 Use:** Automatic reviews when PRs are opened/updated
- **📖 Guide:** [extensions/github-app/README.md](extensions/github-app/README.md)
- **👥 Best For:** Teams, CI/CD workflows, automation
- **🔧 Files:**
  - [app-manifest.json](extensions/github-app/app-manifest.json) - App config
  - [webhook.py](extensions/github-app/webhook.py) - Event handler

### VS Code Extension (For Developers)
- **⏱️ Setup Time:** 10 minutes
- **📍 Use:** Review diffs locally in VS Code
- **📖 Guide:** [extensions/vscode/README.md](extensions/vscode/README.md)
- **👥 Best For:** Development, local workflows
- **🔧 Files:**
  - [package.json](extensions/vscode/package.json) - Extension config
  - [src/extension.ts](extensions/vscode/src/extension.ts) - Main code

---

## ⚙️ Server & API Setup

### Quick Setup
1. [quickstart.sh](quickstart.sh) - Automated setup script
2. [docker-start.sh](docker-start.sh) - Docker quick start

### Server Setup
- **Python:** `python api_server.py`
- **Docker:** `docker-compose up -d`
- **Heroku:** `git push heroku main`
- **See:** [EXTENSION_SETUP.md](EXTENSION_SETUP.md#-deployment-options)

### Configuration
- **Template:** [.env.example](.env.example)
- **Docs:** [EXTENSION_SETUP.md](EXTENSION_SETUP.md#-environment-variables)

### Testing
- **API Test:** `python test_api.py`
- **Manual:** `curl http://localhost:8000/health`

---

## 📚 Detailed Guides

### [EXTENSION_SETUP.md](EXTENSION_SETUP.md) - Complete Reference
- Installation & configuration
- All deployment options
- API endpoints
- Troubleshooting
- Security best practices

### [WEBHOOK_INTEGRATION.md](WEBHOOK_INTEGRATION.md) - GitHub Webhook Integration
- How to integrate webhook into API
- Code examples
- Configuration details

### API Server
- **Main File:** [api_server.py](api_server.py)
- **Endpoints:** `POST /review`, `GET /config`, `POST /webhook/github`
- **Documentation:** Inline docstrings in api_server.py

---

## 🐳 Docker & Deployment

### Docker Files
- [Dockerfile](Dockerfile) - Container image
- [docker-compose.yml](docker-compose.yml) - Full stack (API + DB)

### Scripts
- [quickstart.sh](quickstart.sh) - Quick dev setup
- [docker-start.sh](docker-start.sh) - Docker quick start
- [test_api.py](test_api.py) - API testing script

---

## 📋 File Structure

```
diff-reviewer/
├── 📄 EXTENSIONS_QUICK_START.md         ⭐ Start here
├── 📄 EXTENSION_IMPLEMENTATION_SUMMARY.md  Overview
├── 📄 EXTENSION_SETUP.md                 Full guide
├── 📄 EXTENSION_DOCS_INDEX.md            This file
├── 📄 WEBHOOK_INTEGRATION.md             Webhook guide
├── 📄 api_server.py                      ⭐ API backend
├── 📄 requirements.txt                    Dependencies
├── 📄 .env.example                        Config template
├── 📄 Dockerfile                          Docker image
├── 📄 docker-compose.yml                  Docker compose
├── 📄 quickstart.sh                       Setup script
├── 📄 docker-start.sh                     Docker script
├── 📄 test_api.py                         API tests
│
├── 📁 extensions/
│   ├── 📁 chrome/
│   │   ├── 📄 manifest.json              ⭐ Extension config
│   │   ├── 📄 popup.html                  UI
│   │   ├── 📄 popup.js                    Logic
│   │   ├── 📄 popup.css                   Styling
│   │   ├── 📄 content.js                  GitHub integration
│   │   ├── 📄 background.js               Service worker
│   │   └── 📄 INSTALL_GUIDE.md            Chrome setup
│   │
│   ├── 📁 github-app/
│   │   ├── 📄 app-manifest.json           ⭐ App config
│   │   ├── 📄 webhook.py                  Webhook handler
│   │   └── 📄 README.md                   GitHub App setup
│   │
│   └── 📁 vscode/
│       ├── 📄 package.json                ⭐ Extension config
│       ├── 📄 tsconfig.json               TS config
│       ├── 📄 src/extension.ts            Main code
│       └── 📄 README.md                   VS Code setup
│
└── [existing project files]
```

---

## 🎯 Quick Navigation by Task

### "I want to get started immediately"
→ [EXTENSIONS_QUICK_START.md](EXTENSIONS_QUICK_START.md)

### "I want to use the Chrome extension"
→ [extensions/chrome/INSTALL_GUIDE.md](extensions/chrome/INSTALL_GUIDE.md)

### "I want to set up GitHub App for my team"
→ [extensions/github-app/README.md](extensions/github-app/README.md)

### "I want to develop the VS Code extension"
→ [extensions/vscode/README.md](extensions/vscode/README.md)

### "I want to deploy to production"
→ [EXTENSION_SETUP.md#-deployment-options](EXTENSION_SETUP.md)

### "I want to understand the implementation"
→ [EXTENSION_IMPLEMENTATION_SUMMARY.md](EXTENSION_IMPLEMENTATION_SUMMARY.md)

### "I want API documentation"
→ [api_server.py](api_server.py) docstrings

### "I have a problem"
→ [EXTENSION_SETUP.md#troubleshooting](EXTENSION_SETUP.md)

---

## 📊 Feature Comparison

| Feature | Chrome | GitHub App | VS Code |
|---------|--------|-----------|---------|
| **Setup Time** | 5 min | 20 min | 10 min |
| **Browser Support** | Chrome, Edge | GitHub | VS Code |
| **Auto Review** | ❌ Manual | ✅ Automatic | ❌ Manual |
| **Inline Comments** | ❌ | ✅ | ✅ |
| **Server Required** | ✅ | ✅ | ✅ |
| **Best For** | Individuals | Teams | Developers |
| **Production Ready** | ✅ | ✅ | ⏳ Beta |
| **Web Store Ready** | ⏳ | ⏳ | ⏳ |

---

## 🚀 Deployment Quick Links

### Local Development
```bash
python api_server.py
# Load extension from extensions/[type]/
```

### Docker
```bash
docker-compose up -d
# Then load extension
```

### Heroku
```bash
git push heroku main
```

### Other
See: [EXTENSION_SETUP.md - Deployment Options](EXTENSION_SETUP.md#-deployment-options)

---

## 🔑 Key Concepts

### **API Server** ([api_server.py](api_server.py))
FastAPI backend that:
- Exposes review endpoints
- Handles webhook events
- Manages extension requests
- Communicates with LLMs

### **Chrome Extension** (extensions/chrome/)
Browser extension that:
- Integrates with GitHub
- Sends diffs to API
- Displays reviews in popup
- Stores user settings

### **GitHub App** (extensions/github-app/)
GitHub integration that:
- Receives PR webhooks
- Calls API for reviews
- Posts comments to PRs
- Manages permissions

### **VS Code Extension** (extensions/vscode/)
Editor plugin that:
- Reviews local diffs
- Displays results in webview
- Integrates with command palette
- Manages settings

---

## 🆘 Support & Help

### Documentation
- 📖 Start with [EXTENSIONS_QUICK_START.md](EXTENSIONS_QUICK_START.md)
- 📚 See [EXTENSION_SETUP.md](EXTENSION_SETUP.md) for details
- 🔧 Check [EXTENSION_IMPLEMENTATION_SUMMARY.md](EXTENSION_IMPLEMENTATION_SUMMARY.md)

### Troubleshooting
- [EXTENSION_SETUP.md - Troubleshooting](EXTENSION_SETUP.md#troubleshooting)
- Check browser console (F12) for errors
- Run `python test_api.py` to verify API

### Common Issues

| Issue | Solution |
|-------|----------|
| API connection failed | Check API is running + URL is correct |
| Extension won't load | Verify manifest.json syntax |
| GitHub webhook silent | Check App settings → Advanced → Deliveries |
| Timeout errors | Increase LLM_TIMEOUT_SECONDS in .env |

---

## 📞 Next Steps

1. **Choose extension type** (Chrome/GitHub App/VS Code)
2. **Read the appropriate guide** (links above)
3. **Set up API server** (local, Docker, or cloud)
4. **Load/install extension**
5. **Test with a sample PR**
6. **Deploy to production** (if needed)

---

## ✨ What's New

✅ **API Backend** - FastAPI server for all extensions  
✅ **Chrome Extension** - Full-featured browser extension  
✅ **GitHub App** - Automatic PR reviews  
✅ **VS Code Extension** - Local development integration  
✅ **Docker Support** - Easy deployment  
✅ **Comprehensive Docs** - Complete setup guides  
✅ **Test Suite** - API verification script  

---

**🎉 Your diff-reviewer is now ready to be used as extensions!**

**[Start with Quick Start Guide →](EXTENSIONS_QUICK_START.md)**

