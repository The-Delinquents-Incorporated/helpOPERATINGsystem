# HelpOS

> Privacy-first, offline AI utility engine for scientific computation, tutoring, and local productivity.

---

## Quick Start

```bash
# 1. Clone / open the project
cd "HelpOS Rev2"

# 2. Make the start script executable (first time only)
chmod +x start.sh

# 3. Run
./start.sh
```

Then open **http://localhost:8000** in your browser.

---

## Prerequisites

| Tool | Version | Notes |
|---|---|---|
| Python | 3.9+ | Already on macOS |
| Ollama | Latest | [ollama.com/download](https://ollama.com/download) |
| A local model | Any | `ollama pull llama3` recommended |

### Install Ollama + a model

```bash
# Install Ollama (macOS)
brew install ollama

# Start the Ollama daemon
ollama serve

# Pull a model (in a second terminal)
ollama pull llama3
```

---

## Manual Start (without the script)

```bash
# Create and activate the virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r backend/requirements.txt

# Start the server
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## Run Tests

```bash
.venv/bin/pytest
```

---

## Project Structure

```
HelpOS Rev2/
├── backend/
│   ├── app/
│   │   ├── core/           # Periodic table, constants, chemistry & math stubs
│   │   ├── routes/         # FastAPI route handlers (chat, elements)
│   │   └── services/       # Ollama client, prompt templates, routing coordinator
│   └── requirements.txt
├── frontend/
│   ├── index.html          # App shell
│   ├── css/app.css         # Design system + styles
│   └── js/                 # app.js, chat.js, chemistry.js, utilities.js
├── tests/                  # pytest test suite
├── start.sh                # One-command local launcher
└── plan.md                 # Master project plan
```

---

## Configuration

A default `.env` is included at the project root. You can also create `backend/.env` to override those defaults. HelpOS is local-only by default: the selected model must be installed in the local Ollama daemon and visible from `ollama list` / `/api/tags`.

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
OLLAMA_REQUIRE_LOCAL_MODEL=true
ALLOWED_ORIGINS=["*"]
```

Install the default local model with:

```bash
ollama pull llama3.2:3b
```

---

## Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Frontend app |
| `/api/health` | GET | Server + Ollama status |
| `/api/chat` | POST | Dual-mode AI chat |
| `/api/elements` | GET | All 118 elements |
| `/api/elements/{query}` | GET | Element by symbol, name, or number |
| `/docs` | GET | Interactive API docs (Swagger) |
