import asyncio
import os
import threading
from typing import Optional

import requests

try:
    from openai import AsyncOpenAI
except ModuleNotFoundError:  # pragma: no cover - depends on local environment
    AsyncOpenAI = None

from src.core.config import Settings


class LLMService:
    _rotation_lock = threading.Lock()
    _rotation_index = 0

    def __init__(self, model=None):
        self.settings = Settings.from_env()
        self.provider = self.settings.llm_provider
        self.model = model or self._default_model()
        self.client: Optional[AsyncOpenAI] = None
        self.gemini_api_keys = self._load_gemini_keys()
        self.timeout_seconds = self.settings.llm_timeout_seconds
        self.retry_attempts = self.settings.gemini_retry_attempts
        self.retry_backoff_seconds = self.settings.gemini_retry_backoff_seconds

        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if AsyncOpenAI and api_key:
                self.client = AsyncOpenAI(api_key=api_key)

    @property
    def available(self):
        if self.provider == "gemini":
            return bool(self.gemini_api_keys)
        return self.client is not None

    async def analyze(self, prompt):
        if self.provider == "gemini":
            return await self._analyze_gemini(prompt)
        return await self._analyze_openai(prompt)

    def _default_model(self):
        if self.provider == "gemini":
            return self.settings.gemini_model
        return self.settings.openai_model

    def _load_gemini_keys(self):
        raw_keys = os.getenv("GEMINI_API_KEYS", "")
        return [key.strip() for key in raw_keys.split(",") if key.strip()]

    def _next_gemini_key_order(self):
        with self._rotation_lock:
            start = self._rotation_index
            self._rotation_index = (self._rotation_index + 1) % len(self.gemini_api_keys)

        return [
            self.gemini_api_keys[(start + offset) % len(self.gemini_api_keys)]
            for offset in range(len(self.gemini_api_keys))
        ]

    async def _analyze_openai(self, prompt):
        if not self.client:
            raise RuntimeError(
                "OpenAI service is unavailable. Set OPENAI_API_KEY and install the openai package."
            )

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a senior software engineer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    async def _analyze_gemini(self, prompt):
        if not self.gemini_api_keys:
            raise RuntimeError(
                "Gemini service is unavailable. Set GEMINI_API_KEYS in the environment."
            )

        errors = []
        for attempt in range(self.retry_attempts):
            for api_key in self._next_gemini_key_order():
                try:
                    return await self._post_gemini_request(api_key, prompt)
                except requests.HTTPError as exc:
                    status_code = exc.response.status_code if exc.response is not None else None
                    errors.append(f"HTTP {status_code}")
                    if status_code not in {429, 500, 503}:
                        raise
                except Exception as exc:  # pragma: no cover - network/provider dependent
                    errors.append(exc.__class__.__name__)

            if attempt < self.retry_attempts - 1:
                await asyncio.sleep(self.retry_backoff_seconds * (attempt + 1))

        raise RuntimeError(
            "All Gemini API keys failed for the current request: " + ", ".join(errors)
        )

    async def _post_gemini_request(self, api_key, prompt):
        return await asyncio.to_thread(self._post_gemini_request_sync, api_key, prompt)

    def _post_gemini_request_sync(self, api_key, prompt):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        payload = {
            "systemInstruction": {
                "parts": [
                    {"text": "You are a senior software engineer."}
                ]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt}
                    ],
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json",
                "responseSchema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "severity": {"type": "string"},
                            "category": {"type": "string"},
                            "title": {"type": "string"},
                            "details": {"type": "string"},
                            "confidence": {"type": "string"},
                            "file_path": {"type": "string"},
                        },
                        "required": ["severity", "category", "title", "details", "confidence"],
                    },
                },
                "thinkingConfig": {
                    "thinkingBudget": 0
                }
            },
        }
        response = requests.post(
            url,
            headers={
                "x-goog-api-key": api_key,
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()

        candidates = data.get("candidates") or []
        if not candidates:
            raise RuntimeError("Gemini response did not contain any candidates.")

        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(part.get("text", "") for part in parts if part.get("text"))
        if not text:
            raise RuntimeError("Gemini response did not contain text output.")

        return text
