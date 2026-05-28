import asyncio

from src.loaders.diff_parser import parse_diff
from src.chunking.diff_chunker import DiffChunker
from src.core.logger import get_logger
from src.core.config import Settings

from src.services.llm_service import LLMService
from src.agents.bug_agent import BugAgent
from src.agents.style_agent import StyleAgent
from src.agents.security_agent import SecurityAgent

from src.aggregator.review_aggregator import ReviewAggregator
from src.memory.context_manager import ContextManager


class DiffPipeline:

    def __init__(self, llm=None, chunker=None, agents=None, aggregator=None, memory=None):
        self.settings = Settings.from_env()
        self.logger = get_logger("Pipeline")
        self.chunker = chunker or DiffChunker(settings=self.settings)
        self.llm = llm or LLMService()
        self.agents = agents or {
            "BugAgent": BugAgent(self.llm),
            "StyleAgent": StyleAgent(self.llm),
            "SecurityAgent": SecurityAgent(self.llm),
        }
        self.aggregator = aggregator or ReviewAggregator()
        self.memory = memory or ContextManager()

    async def process_chunk(self, chunk):
        if self._is_docs_only(chunk.files):
            empty_results = {name: [] for name in self.agents}
            self.memory.update("[info] Documentation-only chunk reviewed conservatively with no actionable findings.")
            return empty_results

        context = self.memory.get_context()
        agent_names = list(self.agents.keys())
        tasks = [self.agents[name].run(chunk, context) for name in agent_names]
        results = await asyncio.gather(*tasks)

        output = {}
        for name, result in zip(agent_names, results):
            output[name] = result
            self.memory.update(self._stringify_findings(result))

        return output

    def chunk_diff(self, diff_text):
        files = parse_diff(diff_text)
        return self.chunker.chunk(files)

    def run(self, diff_text):
        return self.chunk_diff(diff_text)

    async def run_async(self, diff_text):
        final_review = await self.run_review_async(diff_text)
        return self.aggregator.render(final_review)

    async def run_review_async(self, diff_text):
        chunks = self.chunk_diff(diff_text)
        all_results = {name: [] for name in self.agents}

        for chunk in chunks:
            chunk_results = await self.process_chunk(chunk)
            for agent_name, result in chunk_results.items():
                all_results[agent_name].append(result)

        merged = {
            k: [finding for chunk_findings in v for finding in chunk_findings]
            for k, v in all_results.items()
        }

        return self.aggregator.aggregate(merged)

    def _stringify_findings(self, findings):
        return "\n".join(
            f"[{finding.normalized_severity()}] {finding.category}: {finding.title} - {finding.details}"
            for finding in findings
        )

    def _is_docs_only(self, files):
        if not files:
            return False

        docs_exts = {".md", ".rst", ".txt"}
        for file_path in files:
            lowered = file_path.lower()
            if lowered.startswith("docs/") or lowered.startswith("doc/"):
                continue
            if lowered.startswith(".github/issue_template/"):
                continue
            if any(lowered.endswith(ext) for ext in docs_exts):
                continue
            return False
        return True
