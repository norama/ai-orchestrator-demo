# Local Development

This document describes how to run the **AI Orchestrator Demo** locally for
development and inspection.

The project is intentionally simple to run and does not require authentication,
background workers, or external services beyond an optional LLM provider.

---

## Tech Stack

**Backend**
- Python 3.13
- FastAPI
- Pydantic
- SQLite (ephemeral, file-based)
- Poetry

**Frontend**
- React
- TypeScript
- Vite
- Tailwind CSS

**AI**
- OpenAI API (pluggable adapter)

---

## Repository Structure

```
backend/
app/
api/
application/
domain/
infrastructure/
tests/

frontend/
src/
api/
components/
data/
types/
```


The backend and frontend are developed as **one system**, not independent apps.
All documentation lives at the repository root.

---

## Prerequisites

- Python 3.13+
- Node.js (LTS recommended)
- Poetry
- npm
- Make

---

## Environment Variables

### Backend

```bash
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
OPENAI_API_KEY=sk-...
```

Notes:

- `OPENAI_API_KEY` is required only for LLM-backed domains
- Deterministic domains work without it

### Frontend

```bash
VITE_API_BASE_URL=http://localhost:8000
```

## Running locally

### Backend

From the repository root:

```bash
make dev-be
```

OpenAPI docs: 
http://localhost:8000/docs

- SQLite storage is local and ephemeral

### Frontend

From the repository root:

```bash
make dev-fe
```

Frontend application:
http://localhost:3000

- Communicates with backend via configured API base URL
- Uses cookies for workspace isolation

## Deployment

- Backend: [Fly.io](https://fly.io/)
- Frontend: [Vercel](https://vercel.com/)
