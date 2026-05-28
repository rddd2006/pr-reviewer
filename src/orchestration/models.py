from dataclasses import dataclass, field

from src.models.review_models import FinalReview


@dataclass(slots=True)
class SupportDoc:
    path: str
    label: str


@dataclass(slots=True)
class PRDigest:
    status: str
    file_count: int
    hunk_count: int
    prioritized_files: list[str] = field(default_factory=list)
    support_docs: list[SupportDoc] = field(default_factory=list)


@dataclass(slots=True)
class PRPlan:
    compression_strategy: str
    prioritized_chunks: int
    question: str | None = None
    wait_for_user: bool = False


@dataclass(slots=True)
class PRRequest:
    diff_text: str
    command: str
    user_request: str = ""
    title: str = ""
    body: str = ""
    is_draft: bool = False


@dataclass(slots=True)
class CommandResult:
    command: str
    result_type: str
    body: str
    digest: PRDigest
    plan: PRPlan
    metadata: dict[str, object] = field(default_factory=dict)
    final_review: FinalReview | None = None

