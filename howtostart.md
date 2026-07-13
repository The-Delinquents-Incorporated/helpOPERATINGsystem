# 🚀 Getting Started with HelpOS

Complete guide to installing, configuring, and launching HelpOS.

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

# 🚀 Quick Start (Recommended)

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

# 📜 Post-Launch Checklist

After starting HelpOS:

- [ ] Application running at `http://localhost:8000`
- [ ] Check health at `/api/health`
- [ ] Verify Ollama is connected and serving llama3.2:3b
- [ ] Access Swagger docs at `/docs`
- [ ] Test AI chat functionality
- [ ] Element database accessible at `/api/elements`

---

# 🔄 Migration / Refresh

If upgrading HelpOS:

```bash
# Refresh the model
ollama pull llama3.2:3b

# Restart FastAPI (Ctrl+C then restart)

# Hard refresh your browser (Ctrl+Shift+R)
```

---

# ❓ Troubleshooting

### Ollama not found
- Ensure Ollama is installed from https://ollama.com/download
- Verify `ollama serve` is running in the background

### Model not found
- Run `ollama pull llama3.2:3b` to download the model
- Check that Ollama daemon is running

### Port 8000 already in use
- Change the port in the `start.sh` script or manual command
- Or kill the process using port 8000 and restart

### Permission denied on start.sh
- Run `chmod +x start.sh` to make it executable

---

For more information, see the main [README.md](README.md)
