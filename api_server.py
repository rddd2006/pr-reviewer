"""
FastAPI backend server for diff-reviewer.
Exposes the review service via HTTP API for Chrome and GitHub extensions.
"""

import os
import json
from pathlib import Path
from typing import Optional
import asyncio

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

from src.orchestration.models import PRRequest
from src.orchestration.service import PRAgentService

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Diff Reviewer API",
    description="LLM-powered PR diff reviewer API",
    version="0.1.0",
)

# Enable CORS for extensions
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "chrome-extension://*",
        "https://github.com",
        "https://github.com/*",
        "http://localhost:3000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service
service = PRAgentService(repo_root=Path.cwd())


class ReviewRequest(BaseModel):
    """Request model for code review."""
    diff: str
    command: str = "review"
    request: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    draft: bool = False
    format: str = "text"


class ReviewResponse(BaseModel):
    """Response model for code review."""
    status: str
    command: str
    result: dict | str
    metadata: Optional[dict] = None


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "diff-reviewer",
        "version": "0.1.0",
    }


@app.post("/review", response_model=ReviewResponse)
async def review_diff(request: ReviewRequest) -> ReviewResponse:
    """
    Review a git diff using the PR agent service.
    
    Args:
        request: ReviewRequest containing diff and command
        
    Returns:
        ReviewResponse with review results
    """
    try:
        # Validate command
        valid_commands = [
            "review", "describe", "ask", "generate_labels", 
            "improve", "update_changelog", "add_doc", 
            "similar_issue", "reflect", "command"
        ]
        if request.command not in valid_commands:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid command. Must be one of: {', '.join(valid_commands)}"
            )
        
        # Create PR request
        pr_request = PRRequest(
            diff=request.diff,
            command=request.command,
            user_request=request.request or "",
            title=request.title or "",
            body=request.body or "",
            draft=request.draft,
        )
        
        # Run review
        result = await service.run(pr_request)
        
        # Format response
        if request.format == "json":
            result_data = result if isinstance(result, dict) else {"result": str(result)}
        else:
            result_data = str(result)
        
        return ReviewResponse(
            status="success",
            command=request.command,
            result=result_data,
            metadata={
                "format": request.format,
                "diff_length": len(request.diff),
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch-review")
async def batch_review(requests: list[ReviewRequest]) -> dict:
    """
    Review multiple diffs in batch.
    
    Args:
        requests: List of ReviewRequest objects
        
    Returns:
        Dictionary mapping index to ReviewResponse
    """
    try:
        results = {}
        for idx, req in enumerate(requests):
            pr_request = PRRequest(
                diff=req.diff,
                command=req.command,
                user_request=req.request or "",
                title=req.title or "",
                body=req.body or "",
                draft=req.draft,
            )
            result = await service.run(pr_request)
            results[str(idx)] = {
                "status": "success",
                "command": req.command,
                "result": str(result)
            }
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/config")
async def get_config():
    """Get configuration info for extensions."""
    return {
        "supported_commands": [
            "review", "describe", "ask", "generate_labels", 
            "improve", "update_changelog", "add_doc", 
            "similar_issue", "reflect"
        ],
        "max_diff_size": 1024 * 1024,  # 1MB
        "timeout_seconds": int(os.getenv("LLM_TIMEOUT_SECONDS", "120")),
    }


@app.get("/version")
async def get_version():
    """Get API version."""
    return {
        "api_version": "0.1.0",
        "service": "diff-reviewer",
    }


if __name__ == "__main__":
    port = int(os.getenv("API_PORT", "8000"))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=os.getenv("ENV", "development") == "development",
    )
