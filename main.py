"""
main.py — FastAPI server entry point for the AI Chatbot.

No API keys or environment variables required.

Routes:
    GET  /         → Serves the chat UI (static/index.html)
    POST /api/chat → Streams a chatbot response (text/plain)
"""

import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn

import agent

app = FastAPI(
    title="ChatBot",
    description="A simple streaming chatbot built with FastAPI.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    """Request body for the /api/chat endpoint."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="The user's message.",
    )


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_ui() -> str:
    """Return the chat UI HTML page."""
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post(
    "/api/chat",
    summary="Stream a chatbot response",
    response_description="Plain-text stream of the bot's reply",
)
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    """Accept a user message and return a streaming plain-text response."""
    return StreamingResponse(
        agent.stream_response(request.message),
        media_type="text/plain",
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
