from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
import httpx

app = FastAPI(title="Pet External API & Product Recommendation Service")

class ProductRecommendation(BaseModel):
    title: str
    shop_name: str
    product_url: str
    suitable_for_allergy: str
    description: str

# Statische Shop- / Produktempfehlungen für Spezialfutter & Snacks
RECOMMENDED_PRODUCTS = [
    {
        "title": "Hypoallergenes Enten-Trockenfutter",
        "shop_name": "FutterFreunde",
        "product_url": "https://example.com/shop/ente-hypoallergen",
        "suitable_for_allergy": "Rind",
        "description": "Ideal für Hunde mit Rinder-Allergie oder sensiblem Magen."
    },
    {
        "title": "Getreidefreie Insekten-Snacks",
        "shop_name": "GreenPet Shop",
        "product_url": "https://example.com/shop/insekten-leckerli",
        "suitable_for_allergy": "Getreide",
        "description": "100% getreidefrei und nachhaltig."
    },
    {
        "title": "Laktosefreie Katzenmilch & Snacks",
        "shop_name": "CatSpecialists",
        "product_url": "https://example.com/shop/laktosefrei-katze",
        "suitable_for_allergy": "Laktose",
        "description": "Speziell für Katzen mit Laktoseintoleranz."
    }
]

@app.get("/random-image")
async def get_random_pet_image(species: str = "Hund"):
    """Holt ein zufälliges Bild über eine externe API (externe Kommunikation)."""
    async with httpx.AsyncClient(timeout=3.0) as client:
        try:
            if species.lower() == "katze":
                # Externe Cat API
                res = await client.get("https://api.thecatapi.com/v1/images/search")
                if res.status_code == 200:
                    data = res.json()
                    return {"image_url": data[0]["url"]}
            else:
                # Externe Dog CEO API
                res = await client.get("https://dog.ceo/api/breeds/image/random")
                if res.status_code == 200:
                    data = res.json()
                    return {"image_url": data.get("message")}
        except Exception:
            pass
            
    # Fallback-Bild, falls externe APIs nicht erreichbar sind (Fault Tolerance)
    return {"image_url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1"}

@app.get("/recommendations", response_model=List[ProductRecommendation])
async def get_recommendations(allergy: Optional[str] = Query(None)):
    """Liefert passende Produkt- & Shop-Links basierend auf Allergien."""
    if allergy:
        filtered = [p for p in RECOMMENDED_PRODUCTS if p["suitable_for_allergy"].lower() == allergy.lower()]
        return filtered if filtered else RECOMMENDED_PRODUCTS
    return RECOMMENDED_PRODUCTS