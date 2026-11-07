from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
import os

app = FastAPI(title="PetCare Frontend Service")
templates = Jinja2Templates(directory="templates")

PET_SERVICE_URL = os.getenv("PET_SERVICE_URL", "http://pet-service:8000")
CALENDAR_SERVICE_URL = os.getenv("CALENDAR_SERVICE_URL", "http://calendar-service:8000")
PET_API_SERVICE_URL = os.getenv("PET_API_SERVICE_URL", "http://pet-api-service:8000")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    pets = []
    image_url = None
    
    async with httpx.AsyncClient(timeout=3.0) as client:
        # 1. Haustiere vom Pet-Service laden
        try:
            resp = await client.get(f"{PET_SERVICE_URL}/pets")
            if resp.status_code == 200:
                pets = resp.json()
        except Exception:
            pass

        # 2. Bild vom API-Service laden (mit Fallback)
        try:
            resp = await client.get(f"{PET_API_SERVICE_URL}/random-image")
            if resp.status_code == 200:
                image_url = resp.json().get("image_url")
        except Exception:
            image_url = "https://images.dog.ceo/breeds/retriever-golden/n02099601_3004.jpg"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "pets": pets,
        "image_url": image_url
    })

@app.post("/pets/{pet_id}/wishlist/{item_id}/buy")
async def buy_wishlist_item(pet_id: int, item_id: int):
    """Leitet den Kaufbefehl an den Pet-Service weiter."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.patch(f"{PET_SERVICE_URL}/pets/{pet_id}/wishlist/{item_id}/buy")
            if response.status_code == 200:
                return {"success": True}
        except Exception:
            pass
    raise HTTPException(status_code=500, detail="Konnte Geschenk nicht als gekauft markieren")