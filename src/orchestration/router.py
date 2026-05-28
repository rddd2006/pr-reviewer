import asyncio

from src.orchestration.models import CommandResult, PRRequest
from src.orchestration.tools import (
    AddDocTool,
    AskTool,
    DescribeTool,
    FutureTool,
    GenerateLabelsTool,
    ImproveTool,
    ReviewTool,
    SimilarIssueTool,
    UpdateChangelogTool,
)


class CommandRouter:
    def __init__(self, pipeline):
        self.tools = {
            "similar_issue": SimilarIssueTool(),
            "review": ReviewTool(pipeline),
            "describe": DescribeTool(),
            "ask": AskTool(),
            "generate_labels": GenerateLabelsTool(),
            "improve": ImproveTool(),
            "update_changelog": UpdateChangelogTool(),
            "add_doc": AddDocTool(),
            "command": FutureTool(),
        }

    async def route(self, request: PRRequest, digest, plan) -> CommandResult:
        if request.command == "reflect":
            return CommandResult(
                command="reflect",
                result_type="PR comment",
                body=plan.question or "",
                digest=digest,
                plan=plan,
                metadata={"wait_for_user": True},
            )

        tool = self.tools.get(request.command)
        if tool is None:
            return CommandResult(
                command=request.command,
                result_type="Empty Result",
                body="Unsupported command.",
                digest=digest,
                plan=plan,
            )

        return await tool.run(request, digest, plan)

