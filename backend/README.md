# Backend

FastAPI backend for the AI chatbot. See [backend.md](../backend.md) for full documentation.

## Quick Start

```bash
# pip
pip install -r requirements_sqlite.txt
uvicorn main_sqlite:app --reload --port 8000

# Poetry
poetry install
poetry run uvicorn main_sqlite:app --reload --port 8000
```

Create `backend/.env`:
```env
ANTHROPIC_API_KEY=your_key
OPENAI_API_KEY=your_key
SECRET_KEY=any_random_string
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

API docs at http://localhost:8000/docs
