from src.core.tokenizer import count_tokens
from src.models.chunk_models import Chunk
from src.chunking.strategies.byte_splitter import split_long_line


def score_line(line):
    if "TODO" in line or "FIXME" in line:
        return -2
    if line.startswith("+"):
        return -1
    return 1


def split_hunk_lines(hunk, file_path, max_tokens):
    lines = sorted(hunk.lines, key=score_line)

    chunks = []
    header = hunk.header + "\n"

    current = header
    current_tokens = count_tokens(current)

    for line in lines:
        tokens = count_tokens(line)

        # ✅ CASE 1: fits
        if current_tokens + tokens <= max_tokens:
            current += line + "\n"
            current_tokens += tokens

        # 🔥 CASE 2: fallback to byte split
        else:
            if tokens > max_tokens:
                line = split_long_line(line, max_tokens)

                if current_tokens + count_tokens(line) <= max_tokens:
                    current += line + "\n"
                    current_tokens += count_tokens(line)

        # flush chunk
        if current_tokens >= max_tokens:
            chunks.append(Chunk(
                content=current,
                tokens=current_tokens,
                files=[file_path]
            ))
            current = header
            current_tokens = count_tokens(current)

    if current_tokens > count_tokens(header):
        chunks.append(Chunk(
            content=current,
            tokens=current_tokens,
            files=[file_path]
        ))

    return chunks
