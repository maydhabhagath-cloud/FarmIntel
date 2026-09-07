from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="FarmIntel API",
    version="2.0.0",
    description="Farm market intelligence prototype for SIH26132.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

CROPS = ["Rice", "Cotton", "Maize", "Tomato", "Groundnut"]

MARKETS = [
    {"market": "Pune APMC", "crop": "Tomato", "price": 2450, "transport": 180, "demand": "High", "distance": 18},
    {"market": "Nashik APMC", "crop": "Tomato", "price": 2520, "transport": 320, "demand": "High", "distance": 42},
    {"market": "Ahmednagar", "crop": "Tomato", "price": 2380, "transport": 250, "demand": "Medium", "distance": 55},
    {"market": "Pune APMC", "crop": "Onion", "price": 2100, "transport": 180, "demand": "Medium", "distance": 18},
]

BUYERS = [
    {"name": "FreshBasket Foods", "crop": "Tomato", "need": "5-10 tonnes", "location": "Pune", "match": 94},
    {"name": "AgroFresh Traders", "crop": "Tomato", "need": "3-8 tonnes", "location": "Nashik", "match": 89},
    {"name": "Local Harvest Co-op", "crop": "Onion", "need": "5-15 tonnes", "location": "Pune", "match": 86},
]

OFFERS = [
    {"buyer": "FreshBasket Foods", "crop": "Tomato", "price": 2500, "quantity": "5 tonnes", "status": "New"},
    {"buyer": "AgroFresh Traders", "crop": "Tomato", "price": 2420, "quantity": "7 tonnes", "status": "Review"},
]

LOTS = [
    {"id": 1, "crop": "Tomato", "quantity": 6, "quality": "Grade A", "location": "Pune", "harvest": "2026-09-12"},
    {"id": 2, "crop": "Onion", "quantity": 10, "quality": "Grade A", "location": "Pune", "harvest": "2026-09-18"},
]


class CropAdviceRequest(BaseModel):
    crop: str = Field(min_length=1, max_length=50)
    soil: str = Field(default="unknown", max_length=80)
    season: str = Field(default="unknown", max_length=80)
    location: str = Field(default="unknown", max_length=120)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


class LotRequest(BaseModel):
    crop: str = Field(min_length=1, max_length=50)
    quantity: float = Field(gt=0, le=100000)
    quality: str = Field(default="Standard", max_length=50)
    location: str = Field(min_length=1, max_length=120)
    harvest: str = Field(min_length=4, max_length=30)


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    index = BASE_DIR / "index.html"
    if not index.exists():
        raise HTTPException(status_code=500, detail="Frontend file is missing")
    return index.read_text(encoding="utf-8")


@app.get("/health")
def health() -> dict:
    return {"status": "healthy", "service": "farmintel", "version": app.version, "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/api/crops")
def crops() -> dict:
    return {"crops": CROPS}


@app.get("/api/markets")
def markets(crop: str | None = None) -> dict:
    rows = MARKETS if not crop else [m for m in MARKETS if m["crop"].lower() == crop.lower()]
    return {"markets": rows}


@app.get("/api/buyers")
def buyers() -> dict:
    return {"buyers": BUYERS}


@app.get("/api/offers")
def offers() -> dict:
    return {"offers": OFFERS}


@app.get("/api/lots")
def lots() -> dict:
    return {"lots": LOTS}


@app.post("/api/lots")
def add_lot(request: LotRequest) -> dict:
    lot = {"id": max((x["id"] for x in LOTS), default=0) + 1, **request.model_dump()}
    LOTS.append(lot)
    return {"lot": lot}


@app.post("/api/crop-advice")
def crop_advice(request: CropAdviceRequest) -> dict:
    crop = request.crop.strip().lower()
    advice = {
        "rice": "Maintain suitable water during key growth stages and scout for blast and stem-borer symptoms.",
        "paddy": "Maintain suitable water during key growth stages and scout for blast and stem-borer symptoms.",
        "cotton": "Scout regularly for sucking pests and bollworms and avoid excessive nitrogen.",
        "maize": "Monitor fall armyworm and maintain adequate moisture around flowering and grain filling.",
        "tomato": "Use balanced irrigation and monitor early blight, late blight and fruit borer.",
        "groundnut": "Monitor leaf spot and soil moisture and avoid prolonged waterlogging.",
    }.get(crop, "Use soil-test-based nutrients, scout for pests, and adjust irrigation to crop stage and local weather.")
    return {"crop": request.crop, "advice": advice, "inputs": request.model_dump(), "source": "FarmIntel demo rule engine"}


@app.post("/api/chat")
def chat(request: ChatRequest) -> dict:
    text = request.message.strip()
    lower = text.lower()
    if any(word in lower for word in ("price", "market", "mandi")):
        reply = "Check Market Intelligence for the current prototype market table and Net Realizable Price calculation."
    elif any(word in lower for word in ("crop", "disease", "pest", "fertilizer")):
        reply = "Use Crop Advice with the crop, soil, season and location to receive an indicative recommendation."
    elif any(word in lower for word in ("buyer", "sell", "offer")):
        reply = "Buyer Matches and Offers show the prototype's matching and offer workflow. Buyer identities are demo data and are not verified."
    else:
        reply = "FarmIntel can help with prototype market comparison, crop advice, buyers and selling decisions."
    return {"reply": reply, "message": text}


@app.get("/api/summary")
def summary() -> dict:
    net_prices = [m["price"] - m["transport"] for m in MARKETS]
    return {
        "active_lots": len(LOTS),
        "offers": len(OFFERS),
        "buyers": len(BUYERS),
        "best_net_price": max(net_prices, default=0),
    }
