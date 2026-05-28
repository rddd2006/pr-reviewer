#!/bin/bash
# Navigation guide for Diff Reviewer Extensions

cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════════════╗
║                   DIFF REVIEWER - EXTENSION NAVIGATION                      ║
║                                                                              ║
║  Your project is now ready as a Chrome Extension, GitHub App, & VS Code Ext  ║
╚══════════════════════════════════════════════════════════════════════════════╝

📍 YOU ARE HERE: diff-reviewer/ root directory

────────────────────────────────────────────────────────────────────────────────
🚀 QUICK START (Pick ONE)
────────────────────────────────────────────────────────────────────────────────

1️⃣  CHROME EXTENSION (Easiest - 5 min)
   📖 Guide: extensions/chrome/INSTALL_GUIDE.md
   🚀 Start: bash quickstart.sh
   ✅ Then:  python api_server.py
   
   Use: Review any GitHub PR in your browser

2️⃣  GITHUB APP (Best for Teams - 20 min)
   📖 Guide: extensions/github-app/README.md
   🚀 Start: docker-compose up -d
   ✅ Then:  Create GitHub App at github.com/settings/apps
   
   Use: Automatic PR reviews for your team

3️⃣  VS CODE EXTENSION (For Developers - 10 min)
   📖 Guide: extensions/vscode/README.md
   🚀 Start: python api_server.py
   ✅ Then:  cd extensions/vscode && npm install && F5
   
   Use: Review diffs locally in VS Code

────────────────────────────────────────────────────────────────────────────────
📚 DOCUMENTATION FILES
────────────────────────────────────────────────────────────────────────────────

✨ START WITH THESE:

  START_HERE.md
  └─ Overview of everything that was built
  └─ Next steps based on your goals
  
  EXTENSIONS_QUICK_START.md
  └─ Quick comparison of extension types
  └─ 5-10 minute quick start guides
  └─ Feature comparison matrix

────────────────────────────────────────────────────────────────────────────────
  THEN READ THESE:

  EXTENSION_SETUP.md
  └─ Comprehensive deployment guide
  └─ All deployment options (Heroku, Docker, AWS Lambda, VPS)
  └─ Environment configuration
  └─ Troubleshooting section
  
  ARCHITECTURE_DIAGRAM.md
  └─ Visual system architecture
  └─ Data flow diagrams
  └─ Component relationships
  
  EXTENSION_DOCS_INDEX.md
  └─ Complete documentation map
  └─ All files and their purposes

────────────────────────────────────────────────────────────────────────────────
  EXTENSION-SPECIFIC GUIDES:

  extensions/chrome/INSTALL_GUIDE.md
  └─ Chrome extension installation
  └─ Development vs production setup
  └─ Publishing to Chrome Web Store
  └─ Troubleshooting Chrome issues
  
  extensions/github-app/README.md
  └─ GitHub App creation
  └─ Webhook configuration
  └─ Deployment steps
  └─ Testing procedures
  
  extensions/vscode/README.md
  └─ VS Code extension development
  └─ Local debugging (F5)
  └─ Marketplace publishing

────────────────────────────────────────────────────────────────────────────────
  TECHNICAL REFERENCE:

  WEBHOOK_INTEGRATION.md
  └─ GitHub webhook handler integration
  └─ Webhook security & verification
  └─ Implementation code examples
  
  EXTENSION_IMPLEMENTATION_SUMMARY.md
  └─ Complete technical implementation details
  └─ Feature breakdown
  └─ Deployment checklist
  
  api_server.py
  └─ FastAPI backend server
  └─ API endpoints documentation
  └─ Start with: python api_server.py

────────────────────────────────────────────────────────────────────────────────
🛠️ QUICK COMMANDS
────────────────────────────────────────────────────────────────────────────────

📦 SETUP & INSTALLATION:

  bash quickstart.sh                 # Automated setup for development
  
  python api_server.py               # Start API server locally
  
  docker-compose up -d               # Start with Docker (recommended)
  
  docker-compose logs -f             # View Docker logs

🧪 TESTING:

  python test_api.py                 # Test API endpoints
  
  curl http://localhost:8000/health  # Quick health check

📂 FILE STRUCTURE:

  ls extensions/chrome/              # View Chrome extension files
  
  ls extensions/github-app/          # View GitHub App files
  
  ls extensions/vscode/              # View VS Code extension files

────────────────────────────────────────────────────────────────────────────────
📊 WHAT WAS CREATED
────────────────────────────────────────────────────────────────────────────────

✅ API BACKEND
   • api_server.py - FastAPI server with REST endpoints
   • Supports: /review, /batch-review, /webhook/github, /config, /health

✅ CHROME EXTENSION (extensions/chrome/)
   • manifest.json - Extension configuration
   • popup.html/popup.js/popup.css - User interface
   • content.js - GitHub page integration
   • background.js - Service worker
   • INSTALL_GUIDE.md - Setup instructions

✅ GITHUB APP (extensions/github-app/)
   • app-manifest.json - GitHub App configuration
   • webhook.py - Event handler
   • README.md - Setup guide

✅ VS CODE EXTENSION (extensions/vscode/)
   • package.json - Extension manifest
   • src/extension.ts - TypeScript implementation
   • README.md - Development guide

✅ DEPLOYMENT & INFRASTRUCTURE
   • Dockerfile - Container image
   • docker-compose.yml - Full dev stack
   • quickstart.sh - Automated setup
   • docker-start.sh - Docker start script
   • test_api.py - API testing

✅ DOCUMENTATION
   • 8+ comprehensive guides
   • Architecture diagrams
   • Troubleshooting sections
   • Quick start references

────────────────────────────────────────────────────────────────────────────────
🎯 COMMON TASKS
────────────────────────────────────────────────────────────────────────────────

"I want to start using it NOW"
  → EXTENSIONS_QUICK_START.md (5 minutes)

"I want to use Chrome extension"
  → extensions/chrome/INSTALL_GUIDE.md

"I want to set up GitHub App for my team"
  → extensions/github-app/README.md

"I want to develop locally"
  → EXTENSIONS_QUICK_START.md (Option 1 or 3)

"I want to deploy to production"
  → EXTENSION_SETUP.md#-deployment-options

"I have an error/problem"
  → EXTENSION_SETUP.md#troubleshooting

"I want to understand the system"
  → ARCHITECTURE_DIAGRAM.md

"I want complete implementation details"
  → EXTENSION_IMPLEMENTATION_SUMMARY.md

"I want API documentation"
  → api_server.py (with docstrings)

────────────────────────────────────────────────────────────────────────────────
🌐 DIRECTORY STRUCTURE
────────────────────────────────────────────────────────────────────────────────

diff-reviewer/
│
├── 📄 START_HERE.md ⭐ (READ THIS FIRST)
├── 📄 EXTENSIONS_QUICK_START.md (Choose your extension type)
├── 📄 EXTENSION_SETUP.md (Complete deployment guide)
├── 📄 ARCHITECTURE_DIAGRAM.md (Visual overview)
├── 📄 EXTENSION_DOCS_INDEX.md (Documentation map)
├── 📄 EXTENSION_IMPLEMENTATION_SUMMARY.md (Technical details)
├── 📄 WEBHOOK_INTEGRATION.md (Webhook guide)
│
├── 📄 api_server.py ⭐ (FastAPI backend)
├── 📄 requirements.txt (Python dependencies)
├── 📄 .env.example (Configuration template)
│
├── 🐳 Dockerfile (Docker image)
├── 🐳 docker-compose.yml (Docker stack)
├── 🚀 quickstart.sh (Setup automation)
├── 🚀 docker-start.sh (Docker automation)
├── 🧪 test_api.py (API testing)
│
├── 📁 extensions/
│   ├── 📁 chrome/ ⭐ (Chrome Extension)
│   │   ├── manifest.json
│   │   ├── popup.html
│   │   ├── popup.js
│   │   ├── popup.css
│   │   ├── content.js
│   │   ├── background.js
│   │   └── INSTALL_GUIDE.md
│   │
│   ├── 📁 github-app/ ⭐ (GitHub App)
│   │   ├── app-manifest.json
│   │   ├── webhook.py
│   │   └── README.md
│   │
│   └── 📁 vscode/ ⭐ (VS Code Extension)
│       ├── package.json
│       ├── tsconfig.json
│       ├── src/extension.ts
│       └── README.md
│
└── [existing project files: src/, tests/, etc.]

────────────────────────────────────────────────────────────────────────────────
⚡ NEXT STEPS
────────────────────────────────────────────────────────────────────────────────

1. Choose your extension type (Chrome/GitHub App/VS Code)
2. Read the appropriate quick start guide
3. Follow the setup instructions
4. Test with a sample PR/diff
5. Deploy to production (if needed)

────────────────────────────────────────────────────────────────────────────────
✅ GETTING STARTED CHECKLIST
────────────────────────────────────────────────────────────────────────────────

[ ] Read START_HERE.md
[ ] Read EXTENSIONS_QUICK_START.md
[ ] Choose your extension type
[ ] Set up API server (local or Docker)
[ ] Load/install extension
[ ] Test with sample PR
[ ] Configure settings
[ ] Deploy to production (optional)

────────────────────────────────────────────────────────────────────────────────
🎓 LEARNING PATH
────────────────────────────────────────────────────────────────────────────────

Beginner → Intermediate → Advanced
   ↓           ↓              ↓
  5 min      20 min        Production
   ↓           ↓              ↓
Quick Start → Full Setup → Customization
   ↓           ↓              ↓
EXTENSIONS_  EXTENSION_   EXTENSION_
QUICK_       SETUP.md     IMPLEMENTATION
START.md                  _SUMMARY.md

────────────────────────────────────────────────────────────────────────────────
📞 HELP & SUPPORT
────────────────────────────────────────────────────────────────────────────────

Problem?                          Solution?
──────────────────────────────────────────────────────────────
Can't get started             →  START_HERE.md
Confused about options        →  EXTENSIONS_QUICK_START.md
Need deployment help          →  EXTENSION_SETUP.md
Want visual overview          →  ARCHITECTURE_DIAGRAM.md
Have an error                 →  EXTENSION_SETUP.md#troubleshooting
Need to understand system     →  EXTENSION_IMPLEMENTATION_SUMMARY.md

────────────────────────────────────────────────────────────────────────────────
🎉 YOU'RE ALL SET!
────────────────────────────────────────────────────────────────────────────────

Your diff-reviewer is ready to be used as a:
  ✅ Chrome Extension (5 minutes)
  ✅ GitHub App (20 minutes)
  ✅ VS Code Extension (10 minutes)

Start with: START_HERE.md

Happy code reviewing! 🚀

────────────────────────────────────────────────────────────────────────────────
EOF

# Show which files were created
echo ""
echo "📋 FILES CREATED:"
echo "───────────────────────────────────────────────────────────────────────────"
ls -la *.md 2>/dev/null | awk '{print "   " $NF}' | grep -E "^   (START|EXTENSION|ARCHITECTURE|WEBHOOK)"
echo ""
echo "🔧 SCRIPTS CREATED:"
echo "───────────────────────────────────────────────────────────────────────────"
ls -la *.sh 2>/dev/null | awk '{print "   " $NF}'
echo ""
echo "🐳 DOCKER FILES:"
echo "───────────────────────────────────────────────────────────────────────────"
ls -la Dockerfile docker-compose.yml 2>/dev/null | awk '{print "   " $NF}'
echo ""
echo "📁 EXTENSIONS CREATED:"
echo "───────────────────────────────────────────────────────────────────────────"
ls -d extensions/*/ 2>/dev/null | awk '{print "   " $0}'
echo ""
