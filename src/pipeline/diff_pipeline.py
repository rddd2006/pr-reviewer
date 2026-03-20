from src.loaders.diff_parser import parse_diff
from src.chunking.diff_chunker import DiffChunker
from src.core.logger import get_logger


class DiffPipeline:

    def __init__(self):
        self.logger = get_logger("Pipeline")
        self.chunker = DiffChunker()

    def run(self, diff_text):
        self.logger.info("Parsing diff")

        files = parse_diff(diff_text)

        self.logger.info(f"Files parsed: {len(files)}")

        chunks = self.chunker.chunk(files)

        return chunks
