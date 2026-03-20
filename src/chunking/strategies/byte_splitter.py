from src.core.tokenizer import count_tokens


def split_long_line(line, max_tokens):
    left, right = 0, len(line)
    best = 0

    while left <= right:
        mid = (left + right) // 2
        part = line[:mid]

        tokens = count_tokens(part)

        if tokens <= max_tokens:
            best = mid
            left = mid + 1
        else:
            right = mid - 1

    return line[:best]
