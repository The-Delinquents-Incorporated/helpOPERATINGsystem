import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.config import settings
from backend.app.routes import elements, chat, chemistry, docs
from backend.app.services.ollama import ollama_service

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Offline-first AI and deterministic calculations engine."
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(elements.router)
app.include_router(chat.router)
app.include_router(chemistry.router)
app.include_router(docs.router)

@app.get("/api/health")
async def health_check():
    """
    Consolidated health status endpoint.
    Checks connection to the local Ollama service.
    """
    ollama_ok = await ollama_service.check_health()
    available_models = []
    
    if ollama_ok:
        models = await ollama_service.list_local_models()
        available_models = [m.get("name") for m in models]
        
    return {
        "status": "healthy",
        "api_version": settings.API_VERSION,
        "release": {
            "version": settings.API_VERSION,
            "label": "0.3: Catalyst",
            "codename": settings.RELEASE_CODENAME,
        },
        "ollama": {
            "connected": ollama_ok,
            "host": settings.OLLAMA_HOST,
            "configured_model": settings.OLLAMA_MODEL,
            "local_only": settings.OLLAMA_REQUIRE_LOCAL_MODEL,
            "available_models": available_models
        }
    }

# Serve frontend static assets
# Resolve path: project root is two levels above backend/app/
_this_dir    = os.path.dirname(os.path.abspath(__file__))          # .../backend/app
_backend_dir = os.path.dirname(_this_dir)                          # .../backend
_project_dir = os.path.dirname(_backend_dir)                       # .../HelpOS Rev2
frontend_dir = os.path.join(_project_dir, "frontend")

if os.path.exists(frontend_dir):
    # Explicit route for root "/" so FastAPI handles it before the StaticFiles mount
    @app.get("/")
    async def serve_index():
        index_path = os.path.join(frontend_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "HelpOS Server is running. No index.html found."}

    # Mount all static assets (CSS, JS, etc.) — html=True handles SPA fallback
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")
else:
    @app.get("/")
    async def root_message():
        return {"message": "HelpOS Server is running. Frontend not yet created."}

