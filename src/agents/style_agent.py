from src.agents.base_agent import BaseAgent
from src.models.review_models import Finding


class StyleAgent(BaseAgent):

    async def run(self, chunk, context):
        prompt = f"""
Review this diff for code quality issues.

Return a JSON array only. Each item must include:
- severity: one of critical, high, medium, low, info
- category
- title
- details
- confidence: one of high, medium, low
- file_path

Report only actionable maintainability, readability, or structural issues that should block or slow approval.
Do not praise the change.
Do not report positive refactors or documentation improvements.
If you do not find a real issue, return [].

Focus on:
- readability
- naming
- structure
- best practices

Context summary:
{context}

DIFF:
{chunk.content}
"""
        return await self._analyze_or_fallback(prompt, chunk, context)

    def fallback(self, chunk, context):
        findings = []
        lines = chunk.content.splitlines()

        if any("TODO" in line or "FIXME" in line for line in lines):
            findings.append(
                Finding(
                    severity="medium",
                    category="maintainability",
                    title="TODO or FIXME added",
                    details="The diff adds unresolved TODO/FIXME markers, which usually indicates incomplete work or deferred cleanup.",
                    confidence="high",
                    file_path=chunk.files[0] if chunk.files else None,
                )
            )
        if any(len(line) > 120 for line in lines):
            findings.append(
                Finding(
                    severity="low",
                    category="readability",
                    title="Long lines added",
                    details="Very long lines reduce readability and make code review harder.",
                    confidence="medium",
                    file_path=chunk.files[0] if chunk.files else None,
                )
            )
        if any(line.strip() == "" for line in lines[-3:]):
            findings.append(
                Finding(
                    severity="low",
                    category="formatting",
                    title="Trailing blank lines added",
                    details="The chunk ends with extra blank lines.",
                    confidence="low",
                    file_path=chunk.files[0] if chunk.files else None,
                )
            )

        return findings
