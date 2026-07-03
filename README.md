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
| A local model | llama3.2:3b (REQUIRED) | You MUST pull this model from Ollama |

### Install Ollama + the required model

```bash
# Install Ollama (macOS)
brew install ollama

# Start the Ollama daemon
ollama serve

# IMPORTANT: You MUST pull the required model before starting HelpOS
# Run this exact command:
ollama pull llama3.2:3b
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

## 0.3: Catalyst Release Notes

HelpOS 0.3 (codename **Catalyst**) focuses on a more polished, responsive, and accessible frontend surface:

- The app shell now visibly identifies the running release as **0.3: Catalyst** in both the sidebar and top bar.
- Navigation and utility tabs include stronger accessibility semantics for keyboard and assistive technology users.
- The health endpoint reports release metadata so frontend and API consumers can confirm the deployed version.

### Migration Checklist

- Restart the FastAPI server after pulling the release so `/api/health` reflects `0.3.0`.
- Hard-refresh the browser if old CSS is cached.
- Confirm the local Ollama model is still available with `ollama pull llama3.2:3b`.

---

## Configuration

A default `.env` is included at the project root. You can also create `backend/.env` to override those defaults. HelpOS is local-only by default: the selected model must be installed in the local Ollama daemon.

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
OLLAMA_REQUIRE_LOCAL_MODEL=true
ALLOWED_ORIGINS=["*"]
```

Install the required local model with:

```bash
ollama pull llama3.2:3b
```

This model is required — HelpOS expects llama3.2:3b to be available locally when OLLAMA_REQUIRE_LOCAL_MODEL is true.

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
