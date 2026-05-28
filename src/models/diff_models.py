from dataclasses import dataclass, field


@dataclass(slots=True)
class Hunk:
    header: str
    lines: list[str] = field(default_factory=list)


@dataclass(slots=True)
class DiffFile:
    path: str
    hunks: list[Hunk] = field(default_factory=list)
