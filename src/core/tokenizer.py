try:
    import tiktoken
except ModuleNotFoundError:  # pragma: no cover - exercised implicitly in tests
    tiktoken = None


if tiktoken:
    try:
        _ENCODER = tiktoken.get_encoding("cl100k_base")
    except Exception:  # pragma: no cover - depends on local tiktoken cache/network
        _ENCODER = None
else:
    _ENCODER = None


def count_tokens(text: str) -> int:
    if not text:
        return 0

    if _ENCODER is not None:
        return len(_ENCODER.encode(text))

    # Conservative fallback when tiktoken is unavailable.
    return max(1, len(text) // 4)
