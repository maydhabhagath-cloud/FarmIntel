from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime, timezone

app = FastAPI(title="FarmIntel API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CropRequest(BaseModel):
    crop: str = Field(min_length=1)
    soil: str = "unknown"
    season: str = "unknown"
    location: str = "unknown"

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)

CROPS = ["Rice", "Cotton", "Maize", "Tomato", "Groundnut", "Onion", "Soybean", "Tur", "Pomegranate"]

ADVICE = {
    "rice": "Maintain appropriate soil moisture during key growth stages and monitor for blast and stem-borer symptoms. Use soil-test-based nutrients.",
    "paddy": "Maintain appropriate soil moisture during key growth stages and monitor for blast and stem-borer symptoms. Use soil-test-based nutrients.",
    "cotton": "Monitor bollworm and sucking pests, avoid excessive nitrogen, and maintain balanced irrigation through flowering and boll development.",
    "maize": "Monitor fall armyworm and maintain irrigation around flowering and grain filling. Use balanced nutrients based on soil testing.",
    "tomato": "Prefer drip irrigation where possible and monitor early/late blight and fruit borer. Avoid prolonged leaf wetness.",
    "groundnut": "Monitor leaf spot and soil moisture; avoid prolonged waterlogging and maintain adequate calcium in the pegging zone.",
    "onion": "Maintain even moisture, avoid waterlogging, and monitor thrips and purple blotch. Reduce irrigation close to harvest.",
    "soybean": "Maintain drainage and monitor defoliators and stem pests. Avoid unnecessary late nitrogen application.",
    "tur": "Monitor pod borer and wilt symptoms, maintain field drainage, and use integrated pest management.",
    "pomegranate": "Monitor bacterial blight and sucking pests, maintain canopy hygiene, and use irrigation appropriate to crop stage.",
}

@app.get("/")
def root():
    return {"name": "FarmIntel API", "status": "online", "version": "1.1.0"}

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

@app.get("/api/crops")
def crops():
    return {"crops": CROPS}

@app.post("/api/crop-advice")
def crop_advice(req: CropRequest):
    crop = req.crop.strip().lower()
    return {
        "crop": req.crop,
        "advice": ADVICE.get(crop, "Use soil-test-based nutrients, monitor pests regularly, and adjust irrigation to crop stage and local weather."),
        "inputs": req.model_dump(),
        "source": "FarmIntel demo rule engine",
    }

@app.post("/api/chat")
def chat(req: ChatRequest):
    message = req.message.strip()
    lower = message.lower()
    if any(x in lower for x in ["price", "market", "mandi", "sell"]):
        reply = "FarmIntel can compare indicative market offers using price, transport, demand and quality fit. Open Market Intelligence or Sell Smart to compare opportunities."
    elif any(x in lower for x in ["pest", "disease", "insect"]):
        reply = "Tell me the crop and the visible pest or disease symptoms. FarmIntel can provide an indicative crop-specific recommendation; field diagnosis should be verified locally."
    elif any(x in lower for x in ["tomato", "cotton", "rice", "maize", "onion", "soybean"]):
        crop = next((c for c in ADVICE if c in lower), None)
        reply = ADVICE[crop] if crop else "Tell me the crop, soil type, season and location for a more targeted recommendation."
    else:
        reply = "I can help with crop advice, market selling decisions, transport considerations and buyer matching. Ask a specific farming question."
    return {"reply": reply, "message": message}
