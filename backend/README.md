# FarmIntel Backend

FastAPI backend for the FarmIntel SIH prototype.

## Run locally

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API endpoints:
- GET `/`
- GET `/health`
- GET `/api/crops`
- POST `/api/crop-advice`
- POST `/api/chat`

Swagger UI is available at `/docs` while the server is running.
