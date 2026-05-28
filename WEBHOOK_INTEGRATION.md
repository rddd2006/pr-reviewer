"""
Integration of webhook handler into the main API server.
This file shows how to add the GitHub webhook to api_server.py
"""

# Add these imports to api_server.py:
# from extensions.github_app.webhook import router as webhook_router

# In the main app setup, add the webhook router:
# app.include_router(webhook_router)

# Or manually add the webhook endpoint:

from fastapi import APIRouter, Request, HTTPException
import hmac
import hashlib
import json
import os

router = APIRouter(prefix="/webhook", tags=["webhooks"])

WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")


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
    """Handle GitHub webhooks."""
    try:
        body = await request.body()
        signature = request.headers.get("X-Hub-Signature-256", "")
        
        if WEBHOOK_SECRET and not verify_webhook_signature(body, signature):
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        payload = json.loads(body)
        event_type = request.headers.get("X-GitHub-Event")
        
        if event_type == "ping":
            return {"message": "pong"}
        
        if event_type == "pull_request":
            action = payload.get("action")
            pr = payload.get("pull_request", {})
            return {
                "status": "received",
                "event": event_type,
                "action": action,
                "pr_number": pr.get("number"),
            }
        
        return {"status": "ignored", "event": event_type}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
