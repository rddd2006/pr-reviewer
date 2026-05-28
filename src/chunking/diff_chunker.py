from src.chunking.strategies.file_packer import FilePacker
from src.chunking.strategies.compression import CompressionStrategy
from src.core.config import Settings
from src.core.logger import get_logger


class DiffChunker:

    def __init__(self, settings=None):
        self.logger = get_logger("DiffChunker")
        self.settings = settings or Settings.from_env()

        self.compression = CompressionStrategy() if self.settings.enable_compression else None
        self.packer = FilePacker(
            max_tokens=self.settings.max_tokens,
            compression=self.compression
        )

    def chunk(self, files):
        self.logger.info("Chunking started")

        chunks = self.packer.pack(files)

        self.logger.info(f"Chunks created: {len(chunks)}")

        return chunks
