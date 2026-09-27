# 🤖 ChatBot — Simple Streaming Chatbot

A lightweight, zero-configuration chatbot built with **FastAPI** (Python) and **vanilla HTML/Tailwind CSS**.

> **No API key required. No external services. Just clone and run.**

---

## ✨ Features

- ⚡ **Real-time streaming** — responses stream word-by-word
- 💬 **Built-in responses** — greetings, jokes, facts, math, and more
- 🧮 **Simple math** — type `2 + 2` or `10 * 5` and get an answer
- 📝 **Markdown rendering** — code blocks, lists, bold/italic
- 📱 **Mobile-responsive** — Tailwind CSS adaptive layout
- 🚨 **Error handling** — network failure banners, 60s timeout
- 🧹 **Clear history** — one-click chat reset
- 🚀 **Render.com ready** — zero environment variables needed

---

## 🗂️ Project Structure

```
ChatBot/
├── main.py            # FastAPI server — routes & streaming endpoint
├── agent.py           # Built-in chatbot logic (no API key needed)
├── requirements.txt   # Python dependencies (only 3 packages)
├── render.yaml        # Render.com deployment blueprint
├── setup.sh           # One-command local setup & launch script
├── .gitignore
└── static/
    └── index.html     # Chat UI (Tailwind CSS + Marked.js + Highlight.js)
```

---

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.10+
- Git

### 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ChatBot.git
cd ChatBot
```

### 2 — Run the setup script

```bash
chmod +x setup.sh
bash setup.sh
```

### Or run manually

```bash
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open **http://localhost:8000** in your browser.

---

## 🌐 Deploy to Render

1. Push this repository to GitHub.
2. Go to [render.com](https://render.com) → **New Web Service** → connect your repo.
3. Render auto-detects `render.yaml`.
4. Click **Deploy** — no environment variables needed.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) |
| Frontend | Vanilla HTML5 + [Tailwind CSS](https://tailwindcss.com/) CDN |
| Markdown | [Marked.js](https://marked.js.org/) |
| Syntax Highlighting | [Highlight.js](https://highlightjs.org/) |
| Deployment | [Render.com](https://render.com) |

---

## 📡 API Reference

### `POST /api/chat`

Streams a chatbot response for the given message.

**Request body:**
```json
{ "message": "Tell me a joke" }
```

**Response:** `text/plain` stream — the bot's reply word-by-word.

### `GET /`

Serves the chat UI (`static/index.html`).

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.
