from src.core.tokenizer import count_tokens
from src.models.chunk_models import Chunk
from src.chunking.strategies.byte_splitter import split_line_into_segments


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
        segments = [line]
        if count_tokens(line) > max_tokens:
            segments = split_line_into_segments(line, max_tokens - count_tokens(header))

        for segment in segments:
            segment_tokens = count_tokens(segment)
            if current_tokens + segment_tokens > max_tokens and current_tokens > count_tokens(header):
                chunks.append(Chunk(
                    content=current,
                    tokens=current_tokens,
                    files=[file_path]
                ))
                current = header
                current_tokens = count_tokens(current)

            current += segment + "\n"
            current_tokens += segment_tokens

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
