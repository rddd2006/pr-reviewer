/**
 * Chrome Extension Popup Script
 */

// DOM Elements
const commandSelect = document.getElementById('command');
const requestGroup = document.getElementById('requestGroup');
const userRequestInput = document.getElementById('userRequest');
const apiUrlInput = document.getElementById('apiUrl');
const apiKeyInput = document.getElementById('apiKey');
const reviewBtn = document.getElementById('reviewBtn');
const saveSettingsBtn = document.getElementById('saveSettingsBtn');
const statusDiv = document.getElementById('status');
const resultDiv = document.getElementById('result');
const resultContent = document.getElementById('resultContent');
const copyBtn = document.getElementById('copyBtn');
const closeResultBtn = document.getElementById('closeResultBtn');

// Event Listeners
commandSelect.addEventListener('change', toggleRequestInput);
reviewBtn.addEventListener('click', handleReview);
saveSettingsBtn.addEventListener('click', handleSaveSettings);
copyBtn.addEventListener('click', handleCopy);
closeResultBtn.addEventListener('click', handleCloseResult);

// Initialize
document.addEventListener('DOMContentLoaded', loadSettings);

/**
 * Toggle request input based on selected command
 */
function toggleRequestInput() {
  const command = commandSelect.value;
  requestGroup.style.display = (command === 'ask') ? 'block' : 'none';
}

/**
 * Load saved settings from storage
 */
function loadSettings() {
  chrome.storage.local.get(['apiUrl', 'apiKey'], (result) => {
    if (result.apiUrl) apiUrlInput.value = result.apiUrl;
    if (result.apiKey) apiKeyInput.value = result.apiKey;
  });
}

/**
 * Save settings to storage
 */
function handleSaveSettings() {
  const apiUrl = apiUrlInput.value.trim();
  
  if (!apiUrl) {
    showStatus('Please enter an API URL', 'error');
    return;
  }

  chrome.storage.local.set(
    {
      apiUrl: apiUrl,
      apiKey: apiKeyInput.value,
    },
    () => {
      showStatus('Settings saved!', 'success');
    }
  );
}

/**
 * Handle review button click
 */
async function handleReview() {
  try {
    const apiUrl = apiUrlInput.value.trim();
    
    if (!apiUrl) {
      showStatus('Please configure API URL first', 'error');
      return;
    }

    showStatus('Fetching PR diff...', 'loading');
    
    // Get active tab
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    const currentTab = tabs[0];

    if (!currentTab.url.includes('github.com')) {
      showStatus('This only works on GitHub.com', 'error');
      return;
    }

    // Extract diff from GitHub
    const diff = await extractGitHubDiff(currentTab.id);
    
    if (!diff) {
      showStatus('Could not extract diff. Make sure you\'re on a PR page.', 'error');
      return;
    }

    showStatus('Sending to AI reviewer...', 'loading');

    // Send to API
    const result = await sendReviewRequest(apiUrl, {
      diff,
      command: commandSelect.value,
      request: userRequestInput.value || undefined,
      format: 'text',
    });

    displayResult(result);
    
  } catch (error) {
    showStatus(`Error: ${error.message}`, 'error');
    console.error('Review error:', error);
  }
}

/**
 * Extract diff from GitHub PR
 */
async function extractGitHubDiff(tabId) {
  try {
    const response = await chrome.tabs.sendMessage(tabId, {
      action: 'getDiff',
    });
    return response.diff;
  } catch (error) {
    console.error('Failed to extract diff:', error);
    return null;
  }
}

/**
 * Send review request to API
 */
async function sendReviewRequest(apiUrl, reviewRequest) {
  const response = await fetch(`${apiUrl}/review`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': apiKeyInput.value ? `Bearer ${apiKeyInput.value}` : '',
    },
    body: JSON.stringify(reviewRequest),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'API request failed');
  }

  return await response.json();
}

/**
 * Display review result
 */
function displayResult(result) {
  hideStatus();
  
  if (typeof result.result === 'string') {
    resultContent.textContent = result.result;
  } else {
    resultContent.textContent = JSON.stringify(result.result, null, 2);
  }
  
  resultDiv.classList.remove('hidden');
  window.scrollTo(0, document.body.scrollHeight);
}

/**
 * Show status message
 */
function showStatus(message, type = 'info') {
  statusDiv.textContent = message;
  statusDiv.className = `status ${type}`;
  statusDiv.classList.remove('hidden');
}

/**
 * Hide status message
 */
function hideStatus() {
  statusDiv.classList.add('hidden');
}

/**
 * Copy result to clipboard
 */
function handleCopy() {
  const text = resultContent.textContent;
  navigator.clipboard.writeText(text).then(() => {
    showStatus('Copied to clipboard!', 'success');
  });
}

/**
 * Close result view
 */
function handleCloseResult() {
  resultDiv.classList.add('hidden');
  hideStatus();
}
