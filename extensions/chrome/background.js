/**
 * Background Service Worker for Chrome Extension
 */

// Listen for tab updates (page navigation)
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url.includes('github.com')) {
    // Inject content script on GitHub pages
    chrome.tabs.sendMessage(tabId, { action: 'pageLoaded' }).catch(() => {
      // Content script might not be ready yet, that's okay
    });
  }
});

// Listen for messages from popup or content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'openReview') {
    chrome.action.openPopup();
  }
});

// Set up alarm for periodic cleanup (optional)
chrome.alarms.create('cleanup', { periodInMinutes: 60 });

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'cleanup') {
    // Clean up old cache entries if needed
    chrome.storage.local.get((items) => {
      const now = Date.now();
      const oneHour = 60 * 60 * 1000;
      
      Object.keys(items).forEach((key) => {
        if (key.startsWith('cache_')) {
          const item = items[key];
          if (item.timestamp && now - item.timestamp > oneHour) {
            chrome.storage.local.remove(key);
          }
        }
      });
    });
  }
});
