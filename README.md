# Local AI API

A FastAPI service exposing a local Ollama model (Gemma 4 26B) as a REST API with streaming, API key auth, and a SvelteKit chat UI.

## Stack

- **Backend**: FastAPI + Ollama (streaming SSE)
- **Frontend**: SvelteKit + TypeScript
- **Model**: gemma4:26b-32k (via Ollama)

## Prerequisites

- [Ollama](https://ollama.com) running locally with `gemma4:26b-32k` pulled:
  ```bash
  ollama pull gemma4:26b-32k
  ```
- Python 3.10+ and Node 18+

## Setup

### Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The API runs at `http://localhost:8000`. Docs at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The UI runs at `http://localhost:5173`.

## API Key

For local development the API key is `dev-key` (set in `.env`).

## Endpoints

### `GET /health`
```bash
curl http://localhost:8000/health
```

### `POST /v1/chat`

Streams the assistant response as Server-Sent Events.

```bash
curl -N http://localhost:8000/v1/chat \
  -H "X-API-Key: dev-key" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain black holes in one paragraph", "system": "You are a concise science communicator."}'
```

**Request body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | Yes* | Simple user message |
| `messages` | array | Yes* | OpenAI-style conversation history (overrides `prompt`) |
| `system` | string | No | System prompt prepended to the conversation |
| `model` | string | No | Override the default model for this request |

*Either `prompt` or `messages` must be provided.

**Response:** `text/event-stream` — each chunk is `data: <token>\n\n`, ending with `data: [DONE]\n\n`.
