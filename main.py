import os
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from fastapi.responses import StreamingResponse
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
app = FastAPI(title="Local AI API")
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
    return {
        "status": "healthy",
        "model": OLLAMA_MODEL
    }

@app.post("/v1/chat")
async def chat(payload: dict, _ = Depends(validate_api_key)):
    prompt = payload.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")

    async def stream_generator():
        async with httpx.AsyncClient(timeout=None) as client:
            try:
                async with client.stream(
                    "POST",
                    OLLAMA_URL,
                    json={
                        "model": OLLAMA_MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                        "stream": True
                    }
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            yield f"{line}\n\n"
            except Exception as e:
                yield f"Error: {str(e)}"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")
