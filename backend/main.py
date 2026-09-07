from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="FarmIntel API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CropRequest(BaseModel):
    crop: str
    soil: str = "unknown"
    season: str = "unknown"
    location: str = "unknown"

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"name": "FarmIntel API", "status": "online", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/crop-advice")
def crop_advice(req: CropRequest):
    # Demo-safe rule engine. Replace with a model/provider later without changing the API contract.
    crop = req.crop.strip().lower()
    advice = {
        "rice": "Maintain adequate standing water during key growth stages and monitor for blast and stem borer symptoms.",
        "paddy": "Maintain adequate standing water during key growth stages and monitor for blast and stem borer symptoms.",
        "cotton": "Monitor for bollworm and sucking pests; avoid excessive nitrogen and maintain balanced irrigation.",
        "maize": "Monitor fall armyworm and maintain irrigation around flowering and grain filling.",
        "tomato": "Use drip irrigation where possible and monitor early blight, late blight and fruit borer.",
        "groundnut": "Monitor leaf spot and soil moisture; avoid prolonged waterlogging.",
    }.get(crop, "Use soil-test-based nutrients, monitor pests regularly, and adjust irrigation to crop stage and local weather.")
    return {"crop": req.crop, "advice": advice, "inputs": req.model_dump()}

@app.post("/api/chat")
def chat(req: ChatRequest):
    message = req.message.strip()
    return {
        "reply": "FarmIntel received your question. For a production AI response, connect this endpoint to your chosen LLM/provider."
        if message else "Please enter a farming question.",
        "message": message,
    }

@app.get("/api/crops")
def crops():
    return {"crops": ["Rice", "Cotton", "Maize", "Tomato", "Groundnut"]}
