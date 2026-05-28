from pathlib import Path

from src.loaders.diff_parser import parse_diff
from src.orchestration.models import PRDigest, PRRequest, SupportDoc


class PRDigestBuilder:
    def build(self, request: PRRequest, repo_root: str | Path = ".") -> PRDigest:
        files = parse_diff(request.diff_text)
        prioritized_files = sorted(
            [diff_file.path for diff_file in files],
            key=self._priority,
            reverse=True,
        )
        hunk_count = sum(len(diff_file.hunks) for diff_file in files)
        return PRDigest(
            status=self._detect_status(request, files),
            file_count=len(files),
            hunk_count=hunk_count,
            prioritized_files=prioritized_files,
            support_docs=self._detect_support_docs(Path(repo_root)),
        )

    def _detect_status(self, request: PRRequest, files):
        if request.is_draft:
            return "draft"
        if not files:
            return "empty"
        if any("wip" in part.lower() for part in [request.title, request.body]):
            return "draft"
        return "ready_for_review"

    def _priority(self, file_path: str):
        lowered = file_path.lower()
        score = 0
        if any(token in lowered for token in ("auth", "security", "secret", "token", "permission")):
            score += 5
        if lowered.endswith((".py", ".ts", ".tsx", ".js", ".java", ".go", ".rb")):
            score += 3
        if "test" not in lowered:
            score += 1
        return score

    def _detect_support_docs(self, repo_root: Path):
        docs = []
        for pattern in ("CONTRIBUTING.md", "contribution.md", "guidelines.md", "GUIDELINES.md"):
            for path in repo_root.rglob(pattern):
                docs.append(SupportDoc(path=str(path.relative_to(repo_root)), label="FUTURE"))
        return sorted(docs, key=lambda doc: doc.path)

