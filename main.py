import json
import os

import httpx
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import APIKeyHeader

load_dotenv()

API_KEY = os.getenv("API_KEY")
app = FastAPI(title="Local AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:4173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def validate_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key",
        )
    return api_key


OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma4:26b-32k")
OLLAMA_URL = "http://localhost:11434/api/chat"


@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": OLLAMA_MODEL}


@app.post("/v1/chat")
async def chat(payload: dict, _=Depends(validate_api_key)):
    messages = payload.get("messages")
    prompt = payload.get("prompt")
    system_prompt = payload.get("system")
    model_override = payload.get("model")

    if messages is None and prompt is None:
        raise HTTPException(
            status_code=400, detail="Either 'prompt' or 'messages' is required"
        )

    chat_messages = []
    if system_prompt:
        chat_messages.append({"role": "system", "content": system_prompt})

    if messages is not None:
        chat_messages.extend(messages)
    elif prompt:
        chat_messages.append({"role": "user", "content": prompt})

    model = model_override if model_override else OLLAMA_MODEL

    async def stream_generator():
        async with httpx.AsyncClient(timeout=None) as client:
            try:
                async with client.stream(
                    "POST",
                    OLLAMA_URL,
                    json={"model": model, "messages": chat_messages, "stream": True},
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                if "message" in data and "content" in data["message"]:
                                    content = data["message"]["content"]
                                    if content:
                                        yield f"data: {content}\n\n"
                                if data.get("done"):
                                    yield "data: [DONE]\n\n"
                            except json.JSONDecodeError:
                                continue
            except Exception as e:
                yield f"data: Error: {str(e)}\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")
