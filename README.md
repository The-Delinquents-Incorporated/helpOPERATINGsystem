# 🧪 HelpOS

![Release](https://img.shields.io/badge/Release-0.4.0--Expansion-blueviolet)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0%2B-009688)
![Ollama](https://img.shields.io/badge/Ollama-llama3.2:3b-orange)
![License](https://img.shields.io/badge/License-HLFL-brightgreen)

> **Privacy-first, offline AI utility engine** for scientific computation, tutoring, and local productivity.

---

# 📦 Prerequisites

| Requirement | Version |
|-------------|----------|
| 🐍 **Python** | **3.9+** |
| 🤖 **Ollama** | **Latest** |
| 🧠 **Model** | **llama3.2:3b (REQUIRED)** |

> **HelpOS is fully offline.**
>
> You **must** have **Ollama** installed and the **llama3.2:3b** model downloaded before launching the application.

---

# 🧰 Required Software

## 🐍 PYTHON

```text
┌──────────────────────────────┐
│  PYTHON                      │
│  Version: 3.9+               │
│  Status: REQUIRED            │
└──────────────────────────────┘
```

---

## 🤖 OLLAMA

```text
┌──────────────────────────────┐
│  OLLAMA                      │
│  Version: Latest             │
│  Status: REQUIRED            │
└──────────────────────────────┘
```

Download:

https://ollama.com/download

---

## 🧠 MODEL

```text
┌──────────────────────────────┐
│  MODEL                       │
│  llama3.2:3b                 │
│  Status: REQUIRED            │
└──────────────────────────────┘
```

Install the model:

```bash
ollama pull llama3.2:3b
```

---

# 🚀 Quick Start

```bash
# Clone / open the repository
cd "HelpOS Rev2"

# Make launcher executable (first run only)
chmod +x start.sh

# Launch HelpOS
./start.sh
```

Open:

```
http://localhost:8000
```

---

# ⚙️ First-Time Setup

## Install Ollama (macOS)

```bash
brew install ollama
```

Start the Ollama daemon:

```bash
ollama serve
```

Download the required model:

```bash
ollama pull llama3.2:3b
```

---

# 🔧 Manual Startup

If you prefer not to use the launcher:

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r backend/requirements.txt

uvicorn backend.app.main:app \
    --host 127.0.0.1 \
    --port 8000 \
    --reload
```

---

# 🧪 Run Tests

```bash
.venv/bin/pytest
```

---

# 📁 Project Structure

```text
HelpOS Rev2
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── routes/
│   │   └── services/
│   └── requirements.txt
│
├── frontend/
│   ├── css/
│   ├── js/
│   └── index.html
│
├── tests/
├── start.sh
└── plan.md
```

---

# ⚙️ Configuration

Default configuration:

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
OLLAMA_REQUIRE_LOCAL_MODEL=true
ALLOWED_ORIGINS=["*"]
```

A root `.env` is included.

Optionally create:

```
backend/.env
```

to override defaults.

---

# 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Frontend |
| `/api/health` | GET | Health & Ollama status |
| `/api/chat` | POST | AI Chat |
| `/api/elements` | GET | All 118 elements |
| `/api/elements/{query}` | GET | Lookup by symbol/name/number |
| `/docs` | GET | Swagger API Documentation |

---

# 🚀 Release

## HelpOS 0.3 — Catalyst

**Catalyst** focuses on polishing the local experience.

### Highlights

- Improved UI responsiveness
- Better accessibility
- Release metadata in API health endpoint
- Refined navigation
- Updated frontend styling

### Migration

```bash
# Refresh the model
ollama pull llama3.2:3b

# Restart FastAPI

# Hard refresh your browser (Ctrl+Shift+R)
```

---

# 💡 Features

- 🔒 Fully Offline
- 🧠 Local LLM via Ollama
- ⚡ FastAPI Backend
- 🧪 Scientific Utilities
- 📚 Chemistry Database
- 💬 AI Chat
- 🧮 Mathematical Computation
- 🖥️ Local-First Architecture

---

# 📜 License

This project is intended for local, privacy-first scientific computing and AI experimentation.
