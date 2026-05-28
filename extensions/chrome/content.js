/**
 * Content Script for GitHub Integration
 */

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getDiff') {
    const diff = extractDiffFromPage();
    sendResponse({ diff: diff || '' });
  }
});

/**
 * Extract diff from GitHub PR page
 */
function extractDiffFromPage() {
  try {
    // Try to get the raw diff URL
    const rawDiffUrl = window.location.href.replace(/\/pull\//, '/pull/').replace(/\/$/, '') + '.patch';
    
    // Alternative: Extract from the page DOM
    const diffElements = document.querySelectorAll('[data-testid="diff-view"]');
    
    if (diffElements.length > 0) {
      // If we're on a PR page, we can construct a diff URL
      const urlParts = window.location.pathname.match(/\/([^/]+)\/([^/]+)\/pull\/(\d+)/);
      if (urlParts) {
        const [, owner, repo, pr] = urlParts;
        // The raw diff is accessible via the GitHub API
        return `# GitHub PR #${pr}\n# Owner: ${owner}/${repo}\n# Please visit: https://github.com/${owner}/${repo}/pull/${pr}.patch`;
      }
    }
    
    return null;
  } catch (error) {
    console.error('Error extracting diff:', error);
    return null;
  }
}

/**
 * Inject review button into GitHub PR page
 */
function injectReviewButton() {
  // Check if we're on a PR page
  if (!window.location.pathname.includes('/pull/')) {
    return;
  }

  // Wait for the page to load
  setTimeout(() => {
    const prHeader = document.querySelector('[data-testid="pull-request-title"]');
    
    if (prHeader && !document.getElementById('diff-reviewer-btn')) {
      const button = document.createElement('button');
      button.id = 'diff-reviewer-btn';
      button.className = 'btn btn-sm';
      button.textContent = '🤖 Review with AI';
      button.style.marginLeft = '10px';
      
      button.addEventListener('click', () => {
        chrome.runtime.sendMessage({ action: 'openReview' });
      });
      
      prHeader.parentNode.insertBefore(button, prHeader.nextSibling);
    }
  }, 1000);
}

// Inject button when page loads
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', injectReviewButton);
} else {
  injectReviewButton();
}

// Also watch for navigation changes (single-page app)
window.addEventListener('popstate', injectReviewButton);
