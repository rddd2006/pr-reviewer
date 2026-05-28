from src.orchestration.digest import PRDigestBuilder
from src.orchestration.models import PRRequest
from src.orchestration.planner import PRPlanner
from src.orchestration.router import CommandRouter
from src.pipeline.diff_pipeline import DiffPipeline


class PRAgentService:
    def __init__(self, pipeline=None, repo_root="."):
        self.pipeline = pipeline or DiffPipeline()
        self.repo_root = repo_root
        self.digest_builder = PRDigestBuilder()
        self.planner = PRPlanner(self.pipeline.chunker)
        self.router = CommandRouter(self.pipeline)

    async def run(self, request: PRRequest):
        digest = self.digest_builder.build(request, repo_root=self.repo_root)
        plan = self.planner.build(request, digest)
        return await self.router.route(request, digest, plan)
