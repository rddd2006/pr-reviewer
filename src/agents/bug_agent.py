from src.agents.base_agent import BaseAgent
from src.models.review_models import Finding


class BugAgent(BaseAgent):

    async def run(self, chunk, context):
        prompt = f"""
You are a bug detection expert.

Return a JSON array only. Each item must include:
- severity: one of critical, high, medium, low, info
- category
- title
- details
- confidence: one of high, medium, low
- file_path

Report only actionable bugs, regressions, or correctness risks introduced or left unresolved by the diff.
Do not praise the change.
Do not report general improvements or documentation wins.
If you do not find a real issue, return [].

Context summary:
{context}

Analyze this diff and find bugs:

{chunk.content}
"""
        return await self._analyze_or_fallback(prompt, chunk, context)

    def fallback(self, chunk, context):
        findings = []
        content = chunk.content

        if "except:" in content:
            findings.append(
                Finding(
                    severity="high",
                    category="reliability",
                    title="Bare except detected",
                    details="Bare except can hide operational failures and make incidents harder to diagnose.",
                    confidence="high",
                    file_path=chunk.files[0] if chunk.files else None,
                )
            )
        if "return True" in content and "return False" not in content:
            findings.append(
                Finding(
                    severity="medium",
                    category="logic",
                    title="Boolean flow appears one-sided",
                    details="The diff returns True without an obvious False path, which can mask failure handling.",
                    confidence="medium",
                    file_path=chunk.files[0] if chunk.files else None,
                )
            )
        if "print(" in content:
            findings.append(
                Finding(
                    severity="low",
                    category="observability",
                    title="Debug printing added",
                    details="Direct print statements can add noisy production logs and bypass structured logging.",
                    confidence="medium",
                    file_path=chunk.files[0] if chunk.files else None,
                )
            )

        return findings
