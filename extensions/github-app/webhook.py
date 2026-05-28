"""
GitHub App webhook handler for diff-reviewer.
"""

from fastapi import APIRouter, Request, HTTPException
import hmac
import hashlib
import json
from typing import Optional

router = APIRouter(prefix="/webhook", tags=["webhooks"])

# Set this to your webhook secret from GitHub App settings
WEBHOOK_SECRET = None  # Set via environment variable


def verify_webhook_signature(request_body: bytes, signature: str) -> bool:
    """Verify GitHub webhook signature."""
    if not WEBHOOK_SECRET:
        return False
    
    expected_signature = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(),
        request_body,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)


@router.post("/github")
async def handle_github_webhook(request: Request):
    """
    Handle GitHub App webhook events.
    
    This endpoint receives events when PRs are opened, updated, or ready for review.
    """
    try:
        # Get the raw body
        body = await request.body()
        
        # Verify signature
        signature = request.headers.get("X-Hub-Signature-256", "")
        if not verify_webhook_signature(body, signature):
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Parse payload
        payload = json.loads(body)
        event_type = request.headers.get("X-GitHub-Event")
        
        if event_type == "pull_request":
            return await handle_pull_request(payload)
        elif event_type == "pull_request_review":
            return await handle_review(payload)
        elif event_type == "ping":
            return {"message": "Pong"}
        
        return {"status": "ignored", "reason": f"Event type {event_type} not handled"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def handle_pull_request(payload: dict):
    """Handle pull request events."""
    action = payload.get("action")
    pr = payload.get("pull_request")
    
    if not pr:
        return {"status": "error", "message": "No PR data"}
    
    if action in ["opened", "synchronize", "reopened"]:
        # New PR or updated - we could auto-review here
        # For now, just acknowledge
        return {
            "status": "acknowledged",
            "pr": pr["number"],
            "action": action,
            "message": "PR registered for review"
        }
    
    return {"status": "ignored", "action": action}


async def handle_review(payload: dict):
    """Handle review events."""
    action = payload.get("action")
    
    return {
        "status": "acknowledged",
        "action": action,
        "message": "Review event received"
    }
