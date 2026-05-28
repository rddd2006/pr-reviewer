from src.chunking.diff_chunker import DiffChunker
from src.loaders.diff_parser import parse_diff
from src.orchestration.models import PRDigest, PRPlan, PRRequest


class PRPlanner:
    def __init__(self, chunker: DiffChunker):
        self.chunker = chunker

    def build(self, request: PRRequest, digest: PRDigest) -> PRPlan:
        chunks = self.chunker.chunk(parse_diff(request.diff_text))
        compression_strategy = "direct"
        prioritized_chunks = max(1, len(chunks)) if chunks else 1

        if digest.file_count > 8 or digest.hunk_count > 20:
            compression_strategy = "token-aware compression and prioritization"

        if request.command == "reflect":
            question = (
                "PR-Agent Planning: I can review more accurately if you clarify the highest-priority concern "
                "for this PR, such as correctness, security, performance, or maintainability."
            )
            return PRPlan(
                compression_strategy=compression_strategy,
                prioritized_chunks=prioritized_chunks,
                question=question,
                wait_for_user=True,
            )

        return PRPlan(
            compression_strategy=compression_strategy,
            prioritized_chunks=prioritized_chunks,
        )
