from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
import os

app = FastAPI(title="PetCare Frontend")
templates = Jinja2Templates(directory="templates")

# URLs zu den internen Backend-Services (über Docker-Netzwerk auflösbar)
PET_SERVICE_URL = os.getenv("PET_SERVICE_URL", "http://pet-service:8000")
CALENDAR_SERVICE_URL = os.getenv("CALENDAR_SERVICE_URL", "http://calendar-service:8000")
PET_API_SERVICE_URL = os.getenv("PET_API_SERVICE_URL", "http://pet-api-service:8000")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    pets = []
    birthdays = []
    random_pet_img = ""

    # Abruf von Daten mit automatischer Fehlertoleranz (Fault Tolerance)
    async with httpx.AsyncClient(timeout=3.0) as client:
        # Fetch Haustiere, Allergien & Wunschlisten
        try:
            res = await client.get(f"{PET_SERVICE_URL}/pets")
            if res.status_code == 200:
                pets = res.json()
        except Exception:
            pets = []  # Fallback bei Ausfall

        # Fetch Geburtstage
        try:
            res = await client.get(f"{CALENDAR_SERVICE_URL}/birthdays")
            if res.status_code == 200:
                birthdays = res.json()
        except Exception:
            birthdays = []  # Fallback bei Ausfall

        # Fetch Zufalls-Tierbild über External Pet API Service
        try:
            res = await client.get(f"{PET_API_SERVICE_URL}/random-image")
            if res.status_code == 200:
                random_pet_img = res.json().get("image_url", "")
        except Exception:
            random_pet_img = ""

    return templates.TemplateResponse("index.html", {
        "request": request,
        "pets": pets,
        "birthdays": birthdays,
        "random_pet_img": random_pet_img
    })