# Chrome Extension - Installation & Usage Guide

## Installation

### Development Mode (Testing)

1. **Prepare the API Server**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   export OPENAI_API_KEY=your-key  # or use .env file
   python api_server.py
   ```
   The API will be available at `http://localhost:8000`

2. **Load the Extension**
   - Open `chrome://extensions` in Chrome
   - Toggle "Developer mode" ON (top right)
   - Click "Load unpacked"
   - Navigate to `extensions/chrome` folder
   - The extension should now appear in your toolbar

3. **Configure Settings**
   - Click the Diff Reviewer extension icon
   - Enter API URL: `http://localhost:8000`
   - Enter API Key (if required): leave blank for local testing
   - Click "Save Settings"

### Production Mode (Publishing to Web Store)

1. **Deploy API Server**

   **Using Heroku:**
   ```bash
   heroku create your-app-name
   heroku buildpacks:set heroku/python
   heroku config:set OPENAI_API_KEY=your-key
   git push heroku main
   ```

   **Using Docker:**
   ```bash
   docker build -t diff-reviewer .
   docker run -p 8000:8000 -e OPENAI_API_KEY=your-key diff-reviewer
   ```

   **Using AWS Lambda:**
   ```bash
   pip install zappa
   zappa init
   zappa deploy production
   ```

2. **Update Extension Configuration**
   - Edit `extensions/chrome/manifest.json`
   - Update `host_permissions` with your production API URL
   - Update `manifest_version` if needed

3. **Build for Distribution**
   ```bash
   # Ensure all code is production-ready
   # Create a zip file
   zip -r diff-reviewer-chrome.zip extensions/chrome/
   ```

4. **Publish to Chrome Web Store**
   - Go to https://chrome.google.com/webstore/devconsole
   - Create a developer account ($5 one-time fee)
   - Click "New Item"
   - Upload `diff-reviewer-chrome.zip`
   - Fill in details:
     - Name: Diff Reviewer
     - Description: AI-powered code review for GitHub PRs
     - Category: Developer Tools
     - Detailed description: [See EXTENSION_SETUP.md]
   - Add screenshots and icon
   - Click "Publish"

## Usage

### Using on GitHub

1. **Navigate to a Pull Request**
   - Go to any PR on github.com

2. **Open Extension**
   - Click the Diff Reviewer icon in toolbar
   - Extension popup will open

3. **Select Review Type**
   - Choose command: `review`, `describe`, `ask`, etc.
   - If `ask` is selected, enter your question

4. **Run Review**
   - Click "Review Current PR"
   - Wait for AI analysis (usually 10-30 seconds)
   - Results appear in the popup

5. **View Results**
   - Review findings are displayed
   - Click "Copy" to copy to clipboard
   - Click "Close" to dismiss

### Keyboard Shortcuts

- `Ctrl+Shift+R` (or `Cmd+Shift+R` on Mac) - Quick review (configurable)

## Features

### Review Commands

| Command | Purpose | Output |
|---------|---------|--------|
| **review** | Full code review with bug, security, style checks | Structured findings with risk scores |
| **describe** | Summarize what changed | Text summary |
| **ask** | Ask a specific question about the code | Text response |
| **generate_labels** | Suggest GitHub labels for the PR | Label suggestions |
| **improve** | Get code improvement suggestions | Inline suggestions |
| **update_changelog** | Generate changelog entry | Markdown text |

### Settings

- **API URL**: Your API server endpoint
- **API Key**: Optional authentication (if your server requires it)
- **Default Command**: Pre-select which review command to use

## Troubleshooting

### "Extension failed to load"
- Check manifest.json for syntax errors
- Ensure all referenced files exist
- Check Chrome console for error messages

### "Cannot connect to API"
- Verify API server is running: `curl http://localhost:8000/health`
- Check API URL is correct in settings
- Ensure CORS is enabled (should be by default)
- Check browser console (F12) for specific errors

### "Diff extraction failed"
- Make sure you're on a GitHub PR page (not issue page)
- Try refreshing the page
- Check browser console for errors
- Ensure you're logged into GitHub

### "Review took too long"
- Increase timeout in API server: `export LLM_TIMEOUT_SECONDS=180`
- Try with a smaller diff
- Check if LLM provider is responding

### "API Key error"
- Verify API key is set in .env or environment
- Check it has proper permissions
- Try regenerating the key
- Ensure key hasn't expired

## Privacy & Security

- **Local Storage**: Extension stores API URL and key in Chrome local storage (encrypted at rest)
- **API Communication**: HTTPS recommended for production
- **Diff Content**: Sent to your API server, ensure you trust it
- **No Tracking**: This extension doesn't track usage

## Data Usage

Each review request sends:
- Git diff content
- PR title (optional)
- PR body (optional)
- Your custom question (optional)

Data is processed by your LLM provider (OpenAI, Google, etc.). Review their privacy policies.

## Advanced Configuration

### Custom API Server

```json
{
  "apiUrl": "https://your-custom-api.com",
  "apiKey": "your-secret-key"
}
```

### Batch Reviews

The API supports batch requests. Edit code to batch multiple PRs.

### Rate Limiting

Set up rate limiting on your API server:
- Heroku: Use middleware
- Docker: Configure nginx
- AWS Lambda: Use API Gateway

## Support

- 📖 See [EXTENSION_SETUP.md](../EXTENSION_SETUP.md) for detailed setup
- 🐛 Report issues on GitHub
- 💬 Check existing issues for solutions

## FAQ

**Q: Is this free?**
A: The extension is free. You only pay for LLM API usage (OpenAI, Google Gemini, etc.)

**Q: Can I use this on private repositories?**
A: Yes! The extension works on private repos if you're authenticated in Chrome.

**Q: Does it work on other git platforms?**
A: Currently GitHub only. GitLab support coming soon.

**Q: How many PRs can I review?**
A: Unlimited, limited only by your LLM provider's rate limits.

**Q: Can I run this offline?**
A: Not with external LLMs. You can set up local LLMs (Ollama, etc.) and point the API to them.

**Q: What data is stored?**
A: Only your API URL and key in local storage. No review history is stored.

---

For more information, see [EXTENSIONS_QUICK_START.md](../EXTENSIONS_QUICK_START.md)
