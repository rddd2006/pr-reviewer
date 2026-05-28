# VS Code Extension Setup

## Development

1. **Install dependencies**:
```bash
cd extensions/vscode
npm install
```

2. **Compile TypeScript**:
```bash
npm run compile
```

3. **Run extension**:
- Press `F5` to open a new VS Code window with the extension loaded

## Configuration

Add to your VS Code `settings.json`:

```json
{
  "diffReviewer.apiUrl": "http://localhost:8000",
  "diffReviewer.apiKey": "",
  "diffReviewer.defaultCommand": "review",
  "diffReviewer.autoReview": false
}
```

## Commands

- `Diff Reviewer: Review Diff` - Review the current file or selected text
- `Diff Reviewer: Review Current File` - Review the active file
- `Diff Reviewer: Open Settings` - Open extension settings

## Publishing

```bash
npm install -g @vscode/vsce
vsce package
vsce publish
```

See [VS Code Extension Publishing](https://code.visualstudio.com/api/working-with-extensions/publishing-extension) for details.
