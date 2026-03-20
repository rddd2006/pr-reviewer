from src.chunking.strategies.file_packer import FilePacker
from src.chunking.strategies.compression import CompressionStrategy
from src.core.config import Settings
from src.core.logger import get_logger


class DiffChunker:

    def __init__(self):
        self.logger = get_logger("DiffChunker")
        self.settings = Settings()

        self.compression = CompressionStrategy()
        self.packer = FilePacker(
            max_tokens=self.settings.MAX_TOKENS,
            compression=self.compression
        )

    def chunk(self, files):
        self.logger.info("Chunking started")

        chunks = self.packer.pack(files)

        self.logger.info(f"Chunks created: {len(chunks)}")

        return chunks
