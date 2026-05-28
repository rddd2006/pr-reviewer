import argparse
import asyncio
import json
from pathlib import Path

from src.orchestration.models import PRRequest
from src.orchestration.service import PRAgentService


def _read_diff(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Run the diff reviewer on a git diff file.")
    parser.add_argument("diff", help="Path to a unified diff file.")
    parser.add_argument(
        "--command",
        default="review",
        choices=[
            "review",
            "describe",
            "ask",
            "generate_labels",
            "improve",
            "update_changelog",
            "add_doc",
            "similar_issue",
            "reflect",
            "command",
        ],
        help="PR-Agent style command to run.",
    )
    parser.add_argument("--request", default="", help="Optional user request or question.")
    parser.add_argument("--title", default="", help="Optional PR title.")
    parser.add_argument("--body", default="", help="Optional PR body.")
    parser.add_argument("--draft", action="store_true", help="Mark the PR as draft.")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format for the review.",
    )
    args = parser.parse_args()

    diff_text = _read_diff(args.diff)
    service = PRAgentService(repo_root=Path.cwd())
    result = asyncio.run(
        service.run(
            PRRequest(
                diff_text=diff_text,
                command=args.command,
                user_request=args.request,
                title=args.title,
                body=args.body,
                is_draft=args.draft,
            )
        )
    )

    if args.format == "json":
        payload = {
            "command": result.command,
            "result_type": result.result_type,
            "body": result.body,
            "digest": {
                "status": result.digest.status,
                "file_count": result.digest.file_count,
                "hunk_count": result.digest.hunk_count,
                "prioritized_files": result.digest.prioritized_files,
                "support_docs": [
                    {"path": doc.path, "label": doc.label}
                    for doc in result.digest.support_docs
                ],
            },
            "plan": {
                "compression_strategy": result.plan.compression_strategy,
                "prioritized_chunks": result.plan.prioritized_chunks,
                "question": result.plan.question,
                "wait_for_user": result.plan.wait_for_user,
            },
            "metadata": result.metadata,
        }
        if result.final_review:
            payload["final_review"] = {
                "total_score": result.final_review.total_score,
                "rating": result.final_review.rating,
                "reviews": [
                    {
                        "agent_name": review.agent_name,
                        "findings": [
                            {
                                "severity": finding.normalized_severity(),
                                "category": finding.category,
                                "title": finding.title,
                                "details": finding.details,
                                "confidence": finding.confidence,
                                "file_path": finding.file_path,
                            }
                            for finding in review.findings
                        ],
                    }
                    for review in result.final_review.reviews
                ],
            }
        print(json.dumps(payload, indent=2))
        return

    print(result.body)


if __name__ == "__main__":
    main()
