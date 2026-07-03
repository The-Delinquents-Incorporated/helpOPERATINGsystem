from typing import Literal, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.services.ollama import ollama_service
from backend.app.services.prompt_templates import DOCS_QUESTIONS_SYSTEM, DOCS_SUMMARY_SYSTEM

router = APIRouter(prefix="/api/docs", tags=["Docs"])


class DocsRequest(BaseModel):
    action: Literal["summary", "questions"] = Field(
        ..., description="Docs action: summarize content or generate study questions"
    )
    text: str = Field(..., min_length=1, description="Document text to process")
    model: Optional[str] = Field(None, description="Optional Ollama model override")


@router.post("")
async def process_document(request: DocsRequest):
    """Generate AI summaries or study questions without tool-routing overhead."""
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Document text cannot be empty.")

    if request.action == "summary":
        system_prompt = DOCS_SUMMARY_SYSTEM
        user_prompt = f"Summarize this document:\n\n{text}"
    else:
        system_prompt = DOCS_QUESTIONS_SYSTEM
        user_prompt = f"Create study questions for this document:\n\n{text}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    try:
        response = await ollama_service.generate_chat_completion(
            messages=messages,
            model=request.model,
            stream=False,
        )
    except RuntimeError as err:
        raise HTTPException(status_code=503, detail=str(err)) from err

    content = response.get("message", {}).get("content", "").strip()
    if not content:
        raise HTTPException(status_code=502, detail="AI returned an empty response.")

    return {
        "mode": "reasoning",
        "action": request.action,
        "content": content,
        "source": "helpos-docs",
    }
