#!/bin/bash
# Quick start script for development

set -e

echo "🚀 Diff Reviewer - Quick Start"
echo "=============================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt

# Copy .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Setting up environment variables..."
    cp .env.example .env
    echo "   Edit .env with your API keys"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📖 Next steps:"
echo "  1. Edit .env with your API keys (OPENAI_API_KEY or GEMINI_API_KEY)"
echo "  2. Start the API server:"
echo "     python api_server.py"
echo "  3. Load the Chrome extension:"
echo "     - Open chrome://extensions"
echo "     - Enable Developer mode"
echo "     - Load unpacked > extensions/chrome"
echo ""
echo "📚 Documentation:"
echo "  - API Setup: EXTENSION_SETUP.md"
echo "  - Chrome Extension: extensions/chrome/manifest.json"
echo "  - GitHub App: extensions/github-app/README.md"
echo ""
