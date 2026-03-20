from src.core.tokenizer import count_tokens
from src.models.chunk_models import Chunk
from src.chunking.strategies.hunk_splitter import split_file_by_hunks


class FilePacker:

    def __init__(self, max_tokens, compression=None):
        self.max_tokens = max_tokens
        self.compression = compression

    def pack(self, files):
        chunks = []

        buffer_content = ""
        buffer_files = []
        current_tokens = 0

        for f in files:
            content = self._serialize(f)
            tokens = count_tokens(content)

            # ✅ CASE 1: fits in current buffer
            if tokens <= self.max_tokens:

                if current_tokens + tokens > self.max_tokens:
                    chunks.append(self._build_chunk(buffer_content, buffer_files))
                    buffer_content = ""
                    buffer_files = []
                    current_tokens = 0

                buffer_content += content + "\n"
                buffer_files.append(f.path)
                current_tokens += tokens

            # 🔥 CASE 2: fallback → hunk splitting
            else:
                split_chunks = split_file_by_hunks(f, self.max_tokens)
                chunks.extend(split_chunks)

        if buffer_files:
            chunks.append(self._build_chunk(buffer_content, buffer_files))

        return chunks

    def _serialize(self, file):
        if self.compression:
            compressed = self.compression.compress(file)
            if compressed:
                return compressed

        text = f"File: {file.path}\n"
        for h in file.hunks:
            text += h.header + "\n"
            text += "\n".join(h.lines) + "\n"

        return text

    def _build_chunk(self, content, files):
        return Chunk(
            content=content,
            tokens=count_tokens(content),
            files=files
        )
