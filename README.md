# 🧪 HelpOS

![Release](https://img.shields.io/badge/Release-0.4.0--Expansion-blueviolet)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0%2B-009688)
![Ollama](https://img.shields.io/badge/Ollama-llama3.2:3b-orange)
![License](https://img.shields.io/badge/License-HLFL-brightgreen)

> **Privacy-first, offline AI utility engine** for scientific computation, tutoring, and local productivity.

---

# 🚀 Quick Start

Ready to launch HelpOS? See **[Getting Started →](howtostart.md)** for complete installation and startup instructions.

---

# 📋 What is HelpOS?

HelpOS is a fully offline, privacy-first AI utility engine built on **local LLMs** via Ollama and a modern FastAPI backend. It's designed for:

- 🧪 Scientific computation
- 📚 Tutoring & learning
- 💬 AI-powered chat
- 🧮 Mathematical utilities
- 🔬 Chemistry database (118 elements)

---

# 💡 Key Features

- 🔒 **Fully Offline** — No cloud dependency
- 🧠 **Local LLM** — Ollama + llama3.2:3b
- ⚡ **FastAPI Backend** — Modern, async Python
- 🧪 **Scientific Utilities** — Computation & analysis
- 📚 **Chemistry Database** — All 118 elements
- 💬 **AI Chat** — Instant answers, offline
- 🧮 **Mathematical Tools** — Symbolic & numerical
- 🖥️ **Local-First Architecture** — Your data stays yours

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
├── plan.md
└── howtostart.md
```

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

# ⚙️ Configuration

Default configuration:

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
OLLAMA_REQUIRE_LOCAL_MODEL=true
ALLOWED_ORIGINS=["*"]
```

A root `.env` is included. Optionally create `backend/.env` to override defaults.

---

# 🚀 Release Notes

## HelpOS 0.4 — Expansion

**Expansion** continues enhancing the local AI experience with new utilities and refined performance.

## HelpOS 0.3 — Catalyst

**Catalyst** focused on polishing the local experience:

- Improved UI responsiveness
- Better accessibility
- Release metadata in API health endpoint
- Refined navigation
- Updated frontend styling

---

# 📜 License

This project is intended for local, privacy-first scientific computing and AI experimentation.
