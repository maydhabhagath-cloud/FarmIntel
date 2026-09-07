# FarmIntel

FarmIntel is a clean full-stack prototype for **SIH26132 — Strengthening market linkages and price discovery for farmers**.

## Architecture

- FastAPI serves both the API and the web application.
- Vanilla HTML/CSS/JavaScript frontend with no build step.
- Railway is the production deployment target.
- A deterministic `railway.toml` defines the build, start command and health check.

## API

- `GET /health` — deployment health check
- `GET /api/summary` — dashboard summary
- `GET /api/crops` — supported crops
- `GET /api/markets` — indicative market opportunities
- `GET /api/lots` / `POST /api/lots` — demo crop-lot workflow
- `GET /api/buyers` — demo buyer matches
- `GET /api/offers` — demo offers
- `POST /api/crop-advice` — rule-based crop advice
- `POST /api/chat` — rule-based farm assistant

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Open `http://127.0.0.1:8000/`.

## Deployment

Railway can deploy directly from the repository root. The repository intentionally keeps `main.py`, `requirements.txt`, `index.html` and `railway.toml` at the root so the platform does not need a nested working directory or implicit start-command detection.

Start command:

```text
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Health check: `/health`.

## Demo limitations

The application uses deterministic in-memory demo data. It does not claim live government feeds, verified buyer identities, guaranteed price forecasts, certified grading, real payments, or production logistics integrations.
