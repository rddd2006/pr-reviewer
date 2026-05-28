from dataclasses import dataclass, field


@dataclass(slots=True)
class Chunk:
    content: str
    tokens: int
    files: list[str] = field(default_factory=list)
