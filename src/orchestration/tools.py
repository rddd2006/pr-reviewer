from src.loaders.diff_parser import parse_diff
from src.orchestration.models import CommandResult


class ReviewTool:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    async def run(self, request, digest, plan):
        final_review = await self.pipeline.run_review_async(request.diff_text)
        return CommandResult(
            command="review",
            result_type="PR comment",
            body=self.pipeline.aggregator.render(final_review),
            digest=digest,
            plan=plan,
            final_review=final_review,
            metadata={"score": final_review.total_score, "rating": final_review.rating},
        )


class DescribeTool:
    async def run(self, request, digest, plan):
        files = parse_diff(request.diff_text)
        changed_paths = [diff_file.path for diff_file in files[:10]]
        body = (
            f"## PR Description\n"
            f"- Status: {digest.status}\n"
            f"- Files changed: {digest.file_count}\n"
            f"- Hunks changed: {digest.hunk_count}\n"
            f"- Focus areas: {', '.join(digest.prioritized_files[:5]) or 'none'}\n"
            f"- Changed files snapshot: {', '.join(changed_paths) or 'none'}"
        )
        return CommandResult(
            command="describe",
            result_type="PR description",
            body=body,
            digest=digest,
            plan=plan,
        )


class AskTool:
    async def run(self, request, digest, plan):
        question = request.user_request.strip() or "What is the main risk in this PR?"
        body = (
            f"## PR Q&A\n"
            f"Question: {question}\n"
            f"Answer: Based on the diff digest, this PR is `{digest.status}` with "
            f"{digest.file_count} changed files and {digest.hunk_count} hunks. "
            f"The highest-priority files appear to be: {', '.join(digest.prioritized_files[:3]) or 'none'}."
        )
        return CommandResult(
            command="ask",
            result_type="PR comment",
            body=body,
            digest=digest,
            plan=plan,
        )


class GenerateLabelsTool:
    async def run(self, request, digest, plan):
        labels = []
        if digest.file_count >= 10 or digest.hunk_count >= 25:
            labels.append("size/large")
        elif digest.file_count >= 4:
            labels.append("size/medium")
        else:
            labels.append("size/small")

        if any("security" in file_path.lower() or "auth" in file_path.lower() for file_path in digest.prioritized_files):
            labels.append("possible security issue")

        effort = min(5, max(1, (digest.file_count + digest.hunk_count) // 5 + 1))
        labels.append(f"review effort {effort}/5")

        return CommandResult(
            command="generate_labels",
            result_type="PR labels",
            body="\n".join(labels),
            digest=digest,
            plan=plan,
            metadata={"labels": labels},
        )


class ImproveTool:
    async def run(self, request, digest, plan):
        suggestions = []
        for file_path in digest.prioritized_files[:3]:
            suggestions.append(
                f"- Suggestion for `{file_path}`: reduce branching, tighten validation, and add targeted tests around modified paths."
            )
        body = "## PR inline code suggestions\n" + ("\n".join(suggestions) if suggestions else "- No suggestions.")
        return CommandResult(
            command="improve",
            result_type="PR inline code suggestions",
            body=body,
            digest=digest,
            plan=plan,
        )


class UpdateChangelogTool:
    async def run(self, request, digest, plan):
        summary = ", ".join(digest.prioritized_files[:5]) or "internal updates"
        body = f"## Changelog\n- Updated PR workflow and code paths touching: {summary}."
        return CommandResult(
            command="update_changelog",
            result_type="Update changelog",
            body=body,
            digest=digest,
            plan=plan,
        )


class AddDocTool:
    async def run(self, request, digest, plan):
        doc_targets = []
        for line in request.diff_text.splitlines():
            if line.startswith("+def ") or line.startswith("+class "):
                doc_targets.append(line[1:].strip())
        body = "## PR inline code suggestions\n"
        if doc_targets:
            body += "\n".join(f"- Add docstring or API comment for `{target}`." for target in doc_targets[:10])
        else:
            body += "- No new public symbols detected for documentation suggestions."
        return CommandResult(
            command="add_doc",
            result_type="PR inline code suggestions",
            body=body,
            digest=digest,
            plan=plan,
        )


class SimilarIssueTool:
    async def run(self, request, digest, plan):
        themes = []
        for file_path in digest.prioritized_files[:5]:
            lowered = file_path.lower()
            if "auth" in lowered or "security" in lowered:
                themes.append("security/authentication regression")
            if "test" in lowered:
                themes.append("test coverage gap")
            if "config" in lowered:
                themes.append("configuration drift")
        if not themes:
            themes.append("No issue tracker integration yet; use this as a placeholder for future semantic issue lookup.")
        body = "## Similar issues\n" + "\n".join(f"- {theme}" for theme in dict.fromkeys(themes))
        return CommandResult(
            command="similar_issue",
            result_type="PR comment",
            body=body,
            digest=digest,
            plan=plan,
        )


class FutureTool:
    async def run(self, request, digest, plan):
        return CommandResult(
            command="command",
            result_type="Empty Result",
            body="FUTURE",
            digest=digest,
            plan=plan,
        )
