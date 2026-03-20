from src.core.tokenizer import count_tokens
from src.models.chunk_models import Chunk
from src.chunking.strategies.line_splitter import split_hunk_lines


def split_file_by_hunks(file, max_tokens):
    chunks = []

    header = f"File: {file.path}\n"
    header_tokens = count_tokens(header)

    current = header
    current_tokens = header_tokens

    for hunk in file.hunks:
        hunk_text = hunk.header + "\n" + "\n".join(hunk.lines) + "\n"
        hunk_tokens = count_tokens(hunk_text)

        # ✅ CASE 1: hunk fits
        if current_tokens + hunk_tokens <= max_tokens:
            current += hunk_text
            current_tokens += hunk_tokens

        else:
            # flush current chunk
            if current_tokens > header_tokens:
                chunks.append(Chunk(
                    content=current,
                    tokens=current_tokens,
                    files=[file.path]
                ))

            # 🔥 CASE 2: hunk too big → fallback to lines
            if hunk_tokens > max_tokens:
                line_chunks = split_hunk_lines(hunk, file.path, max_tokens)
                chunks.extend(line_chunks)

                current = header
                current_tokens = header_tokens

            else:
                current = header + hunk_text
                current_tokens = header_tokens + hunk_tokens

    if current_tokens > header_tokens:
        chunks.append(Chunk(
            content=current,
            tokens=current_tokens,
            files=[file.path]
        ))

    return chunks
