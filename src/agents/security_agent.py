from src.agents.base_agent import BaseAgent
from src.models.review_models import Finding


class SecurityAgent(BaseAgent):

    async def run(self, chunk, context):
        prompt = f"""
Check this diff for security vulnerabilities.

Return a JSON array only. Each item must include:
- severity: one of critical, high, medium, low, info
- category
- title
- details
- confidence: one of high, medium, low
- file_path

Report only actionable security risks introduced or left unresolved by the diff.
Do not praise the change.
Do not report positive documentation or messaging improvements.
If you do not find a real issue, return [].

Focus on:
- injection risks
- auth issues
- unsafe handling

Context summary:
{context}

DIFF:
{chunk.content}
"""
        return await self._analyze_or_fallback(prompt, chunk, context)

    def fallback(self, chunk, context):
        findings = []
        content = chunk.content.lower()

        if "eval(" in content or "exec(" in content:
            findings.append(
                Finding(
                    severity="critical",
                    category="injection",
                    title="Dynamic code execution detected",
                    details="Calls like eval or exec can execute attacker-controlled content and should be removed or heavily constrained.",
                    confidence="high",
                    file_path=chunk.files[0] if chunk.files else None,
                )
            )
        if "shell=true" in content:
            findings.append(
                Finding(
                    severity="high",
                    category="command-execution",
                    title="shell=True detected",
                    details="Using shell=True can introduce command injection risk when command inputs are not tightly controlled.",
                    confidence="high",
                    file_path=chunk.files[0] if chunk.files else None,
                )
            )
        if "select " in content and ("+" in chunk.content or "format(" in chunk.content):
            findings.append(
                Finding(
                    severity="high",
                    category="sql-injection",
                    title="Dynamic query construction detected",
                    details="The query appears to be assembled dynamically. Verify that parameterized queries are used.",
                    confidence="medium",
                    file_path=chunk.files[0] if chunk.files else None,
                )
            )
        if "password" in content or "secret" in content or "api_key" in content:
            findings.append(
                Finding(
                    severity="medium",
                    category="secret-management",
                    title="Sensitive value reference detected",
                    details="The diff mentions credentials or secret material. Confirm these values are not hard-coded or logged.",
                    confidence="medium",
                    file_path=chunk.files[0] if chunk.files else None,
                )
            )

        return findings
