# GitHub App Setup Guide

## Overview

The Diff Reviewer can be deployed as a GitHub App that automatically reviews pull requests when they're opened or updated.

## Prerequisites

- A GitHub account
- A public server to host the webhook
- The API server running and accessible from your GitHub App

## Step 1: Create the GitHub App

1. Go to https://github.com/settings/apps
2. Click "New GitHub App"
3. Fill in the details:
   - **GitHub App name**: Diff Reviewer (or your preferred name)
   - **Homepage URL**: https://github.com/yourusername/diff-reviewer
   - **Webhook URL**: `https://your-server.com/webhook/github`
   - **Webhook secret**: Generate a secure random secret

## Step 2: Configure Permissions

Set the following permissions:

- **Pull requests**: Read & write
- **Contents**: Read-only
- **Checks**: Read & write (if you want to create check runs)

## Step 3: Subscribe to Events

Enable webhook events for:
- Pull request
- Pull request review
- Issues (optional)

## Step 4: Install the App

1. Click "Create GitHub App"
2. Go to the app's settings
3. Click "Install App" and select your repository

## Step 5: Configure Environment Variables

```bash
export GITHUB_APP_ID=your_app_id
export GITHUB_PRIVATE_KEY=your_private_key
export GITHUB_WEBHOOK_SECRET=your_webhook_secret
export API_URL=http://localhost:8000
```

## Step 6: Start the Server

```bash
python api_server.py
```

## How It Works

1. A PR is opened/updated on GitHub
2. GitHub sends a webhook to your server
3. The server fetches the PR diff
4. Sends it to the Diff Reviewer API
5. Posts the review as a GitHub comment

## Testing the Webhook

```bash
curl -X POST http://localhost:8000/webhook/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: ping" \
  -d '{"zen":"Testing..."}'
```

## Troubleshooting

- Check webhook deliveries in GitHub App settings → Advanced → Deliveries
- Enable debug logging: `export LOG_LEVEL=DEBUG`
- Test the API endpoint manually first

## Optional: Create Check Runs

The webhook handler can create GitHub Check Runs to display review results directly in the PR:

```python
# This would require additional GitHub API integration
```

See the webhook.py file for implementation details.
