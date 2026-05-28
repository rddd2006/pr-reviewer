import * as vscode from 'vscode';
import axios, { AxiosInstance } from 'axios';

let apiClient: AxiosInstance;
let outputChannel: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext) {
  outputChannel = vscode.window.createOutputChannel('Diff Reviewer');
  
  // Initialize API client
  const config = vscode.workspace.getConfiguration('diffReviewer');
  const apiUrl = config.get<string>('apiUrl') || 'http://localhost:8000';
  const apiKey = config.get<string>('apiKey');
  
  apiClient = axios.create({
    baseURL: apiUrl,
    headers: {
      'Authorization': apiKey ? `Bearer ${apiKey}` : '',
    },
  });

  // Register commands
  context.subscriptions.push(
    vscode.commands.registerCommand('diffReviewer.reviewDiff', reviewDiff),
    vscode.commands.registerCommand('diffReviewer.reviewCurrentFile', reviewCurrentFile),
    vscode.commands.registerCommand('diffReviewer.openSettings', openSettings),
  );

  outputChannel.appendLine('Diff Reviewer extension activated');
}

async function reviewDiff() {
  try {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage('No active editor');
      return;
    }

    const diff = editor.document.getText();
    
    // Show progress
    await vscode.window.withProgress(
      {
        location: vscode.ProgressLocation.Notification,
        title: 'Reviewing diff...',
        cancellable: false,
      },
      async () => {
        const response = await apiClient.post('/review', {
          diff,
          command: 'review',
          format: 'text',
        });

        // Show result
        const panel = vscode.window.createWebviewPanel(
          'diffReviewResult',
          'Diff Review Result',
          vscode.ViewColumn.Beside,
          { enableScripts: true }
        );

        panel.webview.html = getWebviewContent(response.data.result);
      }
    );
  } catch (error: any) {
    vscode.window.showErrorMessage(`Review failed: ${error.message}`);
    outputChannel.appendLine(`Error: ${error.message}`);
  }
}

async function reviewCurrentFile() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showErrorMessage('No active editor');
    return;
  }

  // For now, this is the same as reviewDiff
  // In a full implementation, you'd get the git diff for this file
  await reviewDiff();
}

function openSettings() {
  vscode.commands.executeCommand('workbench.action.openSettings', 'diffReviewer');
}

function getWebviewContent(result: string): string {
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          line-height: 1.6;
          padding: 20px;
          color: #333;
        }
        pre {
          background: #f5f5f5;
          padding: 12px;
          border-radius: 4px;
          overflow-x: auto;
        }
        h2 { color: #333; }
        .result { white-space: pre-wrap; }
      </style>
    </head>
    <body>
      <h2>Code Review Result</h2>
      <div class="result">${escapeHtml(result)}</div>
    </body>
    </html>
  `;
}

function escapeHtml(text: string): string {
  const map: { [key: string]: string } = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;',
  };
  return text.replace(/[&<>"']/g, (char) => map[char]);
}

export function deactivate() {}
