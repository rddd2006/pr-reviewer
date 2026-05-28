import json
import re

from src.models.review_models import Finding


class BaseAgent:

    def __init__(self, llm_service):
        self.llm = llm_service

    async def _analyze_or_fallback(self, prompt, chunk, context):
        if getattr(self.llm, "available", False):
            raw_response = await self.llm.analyze(prompt)
            return self.parse_response(raw_response, chunk)
        return self.fallback(chunk, context)

    def parse_response(self, raw_response, chunk):
        normalized_response = self._extract_json_payload(raw_response)
        try:
            payload = json.loads(normalized_response)
        except json.JSONDecodeError:
            return [
                Finding(
                    severity="info",
                    category=self.__class__.__name__.replace("Agent", "").lower(),
                    title="Model output was not valid JSON",
                    details=raw_response.strip()[:1000] or "The model returned an empty response.",
                    confidence="low",
                    file_path=chunk.files[0] if chunk.files else None,
                )
            ]

        findings = []
        if not isinstance(payload, list):
            payload = []

        for item in payload:
            if not isinstance(item, dict):
                continue
            findings.append(
                Finding(
                    severity=str(item.get("severity", "info")),
                    category=str(item.get("category", "general")),
                    title=str(item.get("title", "Untitled finding")),
                    details=str(item.get("details", "")),
                    confidence=str(item.get("confidence", "medium")),
                    file_path=item.get("file_path") or (chunk.files[0] if chunk.files else None),
                )
            )

        return findings

    def _extract_json_payload(self, raw_response):
        text = raw_response.strip()
        if text.startswith("```"):
            fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
            if fenced:
                return fenced.group(1).strip()

        first_array = text.find("[")
        last_array = text.rfind("]")
        if first_array != -1 and last_array != -1 and first_array < last_array:
            return text[first_array:last_array + 1]

        first_object = text.find("{")
        last_object = text.rfind("}")
        if first_object != -1 and last_object != -1 and first_object < last_object:
            return text[first_object:last_object + 1]

        return text

    def fallback(self, chunk, context):
        raise NotImplementedError

    async def run(self, chunk, context):
        raise NotImplementedError
