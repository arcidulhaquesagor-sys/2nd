"""
agent.py — Simple built-in chatbot. No API key required.

Uses keyword-based pattern matching to generate responses.
Fully self-contained — no external services or credentials needed.
"""

import asyncio
import random
from collections.abc import AsyncGenerator


# ── Response map ─────────────────────────────────────────────────
RESPONSES: dict[str, list[str]] = {
    # Greetings
    ("hello", "hi", "hey", "howdy", "hiya", "sup", "what's up"): [
        "Hey there! 👋 How can I help you today?",
        "Hello! Great to see you. What's on your mind?",
        "Hi! I'm ready to chat. What would you like to talk about?",
    ],
    # Farewells
    ("bye", "goodbye", "see you", "later", "cya", "farewell", "take care"): [
        "Goodbye! Have a wonderful day! 👋",
        "See you later! Take care! 😊",
        "Bye! Feel free to come back anytime. 🙌",
    ],
    # How are you
    ("how are you", "how's it going", "how do you do", "you okay", "you good"): [
        "I'm doing great, thanks for asking! How about you? 😊",
        "Running smoothly and ready to chat! How are you doing?",
        "All good here! What can I do for you today?",
    ],
    # Name
    ("your name", "who are you", "what are you", "what's your name"): [
        "I'm **ChatBot** — a simple AI assistant here to help you! 🤖",
        "You can call me **ChatBot**! I'm here to answer your questions.",
    ],
    # Help
    ("help", "what can you do", "capabilities", "features", "assist"): [
        (
            "I can help with:\n"
            "- 💬 Answering general questions\n"
            "- 🧮 Basic math (`2 + 2`, `10 * 5`)\n"
            "- 😄 Jokes and fun facts\n"
            "- 🕐 Current time info\n"
            "- 💡 General advice\n\n"
            "Just type anything and I'll do my best!"
        ),
    ],
    # Thanks
    ("thank", "thanks", "thank you", "thx", "appreciate", "cheers"): [
        "You're welcome! 😊 Anything else I can help with?",
        "Happy to help! Let me know if you need anything else. 🙌",
        "Anytime! That's what I'm here for. ✨",
    ],
    # Jokes
    ("joke", "funny", "make me laugh", "tell me a joke", "humor"): [
        "Why don't scientists trust atoms? Because they make up everything! 😄",
        "Why did the programmer quit his job? Because he didn't get arrays! 🤣",
        "What do you call a fake noodle? An impasta! 😂",
        "Why can't a bicycle stand on its own? It's two-tired! 😆",
        "I told my computer I needed a break — now it won't stop sending me KitKat ads. 😅",
    ],
    # Facts
    ("fact", "fun fact", "did you know", "interesting", "tell me something"): [
        "🐙 Octopuses have three hearts and blue blood!",
        "🍯 Honey never spoils — archaeologists found 3000-year-old honey in Egyptian tombs that was still edible!",
        "🌍 The Earth's core is as hot as the surface of the Sun (~5,500°C).",
        "🐦 A group of flamingos is called a 'flamboyance'. How fitting!",
        "💡 The first computer bug was an actual bug — a moth found in a Harvard relay in 1947.",
    ],
    # Weather
    ("weather", "temperature", "forecast", "rain", "sunny"): [
        "I don't have access to live weather data, but you can check **weather.com** or just ask your phone's assistant! ☀️🌧️",
    ],
    # Time / Date
    ("time", "date", "today", "what day", "current time"): [
        "I don't have a live clock, but your device's clock is always accurate! ⏰",
    ],
    # Meaning of life
    ("meaning of life", "42", "purpose", "why are we here"): [
        "The answer to life, the universe, and everything is... **42**. 🌌 (Thanks, Douglas Adams!)",
        "That's a deep one! I think it's about connection, curiosity, and the occasional cup of coffee. ☕",
    ],
    # AI / self
    ("are you ai", "are you a robot", "are you real", "are you human", "are you smart"): [
        "I'm a simple rule-based chatbot — no AI magic, just pattern matching! 🤖 But I try my best.",
        "I'm a chatbot built with Python and FastAPI. Simple, but friendly! 😊",
    ],
    # Math (handled separately in logic below)
}

# Flat lookup: keyword → responses list
_FLAT: dict[str, list[str]] = {}
for keywords, replies in RESPONSES.items():
    for kw in keywords:
        _FLAT[kw] = replies

FALLBACKS = [
    "Hmm, I'm not sure about that one. Could you rephrase? 🤔",
    "Interesting question! I'm a simple bot and might not have the answer, but try me again! 💬",
    "I didn't quite get that. Could you try asking differently?",
    "That's beyond my current knowledge! Try asking something else. 🙂",
    "Good question — sadly I don't have an answer for that yet. 😅",
]


def _try_math(text: str) -> str | None:
    """Attempt to evaluate a simple arithmetic expression."""
    import re
    expr = re.sub(r"[^0-9+\-*/().\s]", "", text).strip()
    if not expr or not any(op in expr for op in "+-*/"):
        return None
    try:
        result = eval(expr, {"__builtins__": {}})  # noqa: S307
        return f"🧮 `{expr}` = **{result}**"
    except Exception:
        return None


def _build_reply(message: str) -> str:
    lower = message.lower().strip()

    # Math check first
    math_result = _try_math(lower)
    if math_result:
        return math_result

    # Keyword match (longest match wins)
    matched: list[str] | None = None
    matched_len = 0
    for kw, replies in _FLAT.items():
        if kw in lower and len(kw) > matched_len:
            matched = replies
            matched_len = len(kw)

    if matched:
        return random.choice(matched)

    return random.choice(FALLBACKS)


async def stream_response(message: str) -> AsyncGenerator[str, None]:
    """
    Yield a response word-by-word to simulate streaming.
    No external API or credentials required.
    """
    reply = _build_reply(message)
    words = reply.split(" ")
    for i, word in enumerate(words):
        yield word + (" " if i < len(words) - 1 else "")
        await asyncio.sleep(0.04)   # ~25 words/sec typing feel
