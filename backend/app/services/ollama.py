import json
from typing import AsyncGenerator, Dict, List, Any, Optional
import httpx
from backend.app.config import settings

class OllamaService:
    def __init__(self, host: str = settings.OLLAMA_HOST, default_model: str = settings.OLLAMA_MODEL):
        self.host = host.rstrip("/")
        self.default_model = default_model

    async def check_health(self) -> bool:
        """
        Check if local Ollama instance is running and reachable.
        """
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(f"{self.host}/")
                return response.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException):
            return False

    async def list_local_models(self) -> List[Dict[str, Any]]:
        """
        List all models pulled/available on the local Ollama instance.
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.host}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    return data.get("models", [])
                return []
        except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPError):
            return []

    async def resolve_model(self, requested_model: Optional[str] = None) -> str:
        """Return an available local model, honoring explicit .env/request overrides first."""
        preferred = (requested_model or self.default_model or "").strip()
        models = await self.list_local_models()
        names = [m.get("name") or m.get("model") for m in models]
        names = [name for name in names if name]

        if not names:
            return preferred or "llama3"

        if preferred in names:
            return preferred

        preferred_latest = f"{preferred}:latest" if preferred and ":" not in preferred else preferred
        if preferred_latest in names:
            return preferred_latest

        short_matches = [name for name in names if preferred and name.split(":", 1)[0] == preferred.split(":", 1)[0]]
        if short_matches:
            return short_matches[0]

        return names[0]

    async def generate_chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: str = None, 
        stream: bool = False
    ) -> Any:
        """
        Send chat completion request to Ollama's /api/chat endpoint.
        If stream=True, returns an AsyncGenerator yielding chunks.
        If stream=False, returns the complete response dictionary.
        """
        # First, ensure Ollama is available
        if not await self.check_health():
            raise RuntimeError(f"Ollama instance at {self.host} is unreachable. Please verify it is running.")

        selected_model = await self.resolve_model(model)
        url = f"{self.host}/api/chat"
        payload = {
            "model": selected_model,
            "messages": messages,
            "stream": stream
        }

        if stream:
            return self._stream_completion(url, payload)
        else:
            return await self._non_stream_completion(url, payload)

    async def _non_stream_completion(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload)
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                detail = self._ollama_error_detail(exc.response)
                raise RuntimeError(detail) from exc
            return response.json()

    async def _stream_completion(self, url: str, payload: Dict[str, Any]) -> AsyncGenerator[str, None]:
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", url, json=payload) as response:
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError as exc:
                    detail = self._ollama_error_detail(exc.response)
                    raise RuntimeError(detail) from exc
                async for line in response.aiter_lines():
                    if line:
                        try:
                            # Verify it is valid JSON before yielding
                            chunk = json.loads(line)
                            yield line
                        except json.JSONDecodeError:
                            continue

    def _ollama_error_detail(self, response: httpx.Response) -> str:
        try:
            body = response.json()
            message = body.get("error") or body.get("detail") or response.text
        except ValueError:
            message = response.text
        return f"Ollama request failed ({response.status_code}) for {self.host}: {message}"

ollama_service = OllamaService()
