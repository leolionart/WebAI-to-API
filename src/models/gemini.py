# src/models/gemini.py
import asyncio
from typing import Optional, List, Union
from pathlib import Path
from gemini_webapi import GeminiClient as WebGeminiClient
from app.config import CONFIG
from app.logger import logger

# Errors that are transient — gemini-webapi auto-reinits the session after
# these, so retrying after a short delay usually succeeds.
_RETRYABLE_KEYWORDS = ("zombie stream", "failed to parse response body", "stalled")
_MAX_RETRIES = 2
_RETRY_DELAYS = (3.0, 5.0)  # seconds between retry attempts


class MyGeminiClient:
    """
    Wrapper for the Gemini Web API client with automatic retry on
    transient errors (zombie stream / parse failures) and dynamic model resolution.
    """
    def __init__(self, secure_1psid: str, secure_1psidts: str, proxy: str | None = None) -> None:
        self.client = WebGeminiClient(secure_1psid, secure_1psidts, proxy)

    def _resolve_model(self, model: str) -> str:
        """Resolve generic or legacy model names against gemini-webapi dynamic model registry."""
        if not hasattr(self.client, "_model_registry") or not self.client._model_registry:
            return model
        reg = self.client._model_registry
        if model in reg:
            return model

        model_lower = str(model).lower()
        if "thinking" in model_lower:
            for k in reg:
                if "thinking" in k.lower():
                    return k
        if "pro" in model_lower:
            for k in reg:
                if "hydrogen" in k.lower() and "thinking" not in k.lower():
                    return k
                if "pro" in k.lower():
                    return k
        for k in reg:
            if "neon" in k.lower() or "flash" in k.lower():
                return k
        return next(iter(reg.keys()))

    async def init(self) -> None:
        """Initialize the Gemini client."""
        # Prevent gemini-webapi from falsely blocking multimodal requests when
        # optional enterprise/quota RPCs return permission denied on personal accounts.
        def _safe_check_account_status(raise_error: bool = False) -> bool:
            return True

        self.client._check_account_status = _safe_check_account_status
        await self.client.init()

    async def generate_content(self, message: str, model: str, files: Optional[List[Union[str, Path]]] = None):
        """
        Generate content with automatic retry on transient errors.
        gemini-webapi reinitializes its session after zombie/parse errors
        (~2-3 s); retrying after that window succeeds in most cases.
        """
        resolved_model = self._resolve_model(model)
        last_exc: Exception | None = None
        for attempt in range(_MAX_RETRIES + 1):
            try:
                return await self.client.generate_content(message, model=resolved_model, files=files)
            except Exception as e:
                last_exc = e
                err_lower = str(e).lower()
                is_retryable = any(kw in err_lower for kw in _RETRYABLE_KEYWORDS)
                if is_retryable and attempt < _MAX_RETRIES:
                    delay = _RETRY_DELAYS[attempt]
                    logger.warning(
                        f"Gemini transient error (attempt {attempt + 1}/{_MAX_RETRIES + 1},"
                        f" model={resolved_model}): {e!r} — retrying in {delay}s"
                    )
                    await asyncio.sleep(delay)
                    continue
                # Non-retryable or exhausted retries
                raise
        raise last_exc  # unreachable, satisfies type checkers

    async def close(self) -> None:
        """Close the Gemini client."""
        await self.client.close()

    def start_chat(self, model: str):
        """
        Start a chat session with the given model.
        """
        resolved_model = self._resolve_model(model)
        return self.client.start_chat(model=resolved_model)
