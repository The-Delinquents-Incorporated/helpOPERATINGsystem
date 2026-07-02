from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from backend.app.services.coordinator import coordinator_service

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the message sender ('user', 'assistant', 'system')")
    content: str = Field(..., description="Content of the message")

class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., description="Conversation history")
    model: Optional[str] = Field(None, description="Ollama model to use. Defaults to configured setting.")
    stream: bool = Field(False, description="Whether to stream the response or not")

@router.post("")
async def chat_completion(request: ChatRequest):
    """
    Generate chat response using HelpOS Routing Coordinator (Reasoning Mode vs. Deterministic calculations).
    """
    messages_payload = [m.model_dump() for m in request.messages]
    
    try:
        if request.stream:
            # Route and stream through the coordinator
            generator = coordinator_service.route_query_stream(
                messages=messages_payload,
                model=request.model
            )
            
            async def event_generator():
                try:
                    async for chunk in generator:
                        yield f"{chunk}\n"
                except Exception as stream_err:
                    yield f"{{\"mode\": \"error\", \"detail\": \"{str(stream_err)}\", \"done\": true}}\n"
            
            return StreamingResponse(event_generator(), media_type="application/x-ndjson")
            
        else:
            # Route and get response through the coordinator
            response = await coordinator_service.route_query(
                messages=messages_payload,
                model=request.model
            )
            return response
            
    except RuntimeError as r_err:
        raise HTTPException(status_code=503, detail=str(r_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Failed to process chat request: {str(err)}")

