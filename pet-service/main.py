from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Pet & Wishlist Backend Service")

class WishlistItem(BaseModel):
    id: int
    item_name: str
    category: str
    status: str = "offen"  # "offen" oder "gekauft"

class Pet(BaseModel):
    id: int
    name: str
    species: str
    breed: str
    allergies: List[str] = []
    wishlist: List[WishlistItem] = []

class PetCreate(BaseModel):
    name: str
    species: str
    breed: str
    allergies: Optional[List[str]] = []

class WishlistCreate(BaseModel):
    item_name: str
    category: str

# In-Memory Datenbank
pets_db = [
    {
        "id": 1,
        "name": "Bello",
        "species": "Hund",
        "breed": "Goldendoodle",
        "allergies": ["Rind", "Getreide"],
        "wishlist": [
            {"id": 101, "item_name": "Hypoallergenes Enten-Leckerli", "category": "Snack", "status": "offen"},
            {"id": 102, "item_name": "KONG Spielzeug", "category": "Spielzeug", "status": "gekauft"}
        ]
    },
    {
        "id": 2,
        "name": "Luna",
        "species": "Katze",
        "breed": "Siam",
        "allergies": ["Laktose"],
        "wishlist": [
            {"id": 201, "item_name": "Lachs-Snack Pastete", "category": "Snack", "status": "offen"}
        ]
    }
]

@app.get("/pets", response_model=List[Pet])
async def get_all_pets():
    return pets_db

@app.post("/pets", response_model=Pet, status_code=status.HTTP_201_CREATED)
async def create_pet(pet: PetCreate):
    """Erstellt ein neues Haustier-Profil."""
    new_id = max([p["id"] for p in pets_db], default=0) + 1
    new_pet = {
        "id": new_id,
        "name": pet.name,
        "species": pet.species,
        "breed": pet.breed,
        "allergies": pet.allergies or [],
        "wishlist": []
    }
    pets_db.append(new_pet)
    return new_pet

@app.post("/pets/{pet_id}/wishlist", response_model=WishlistItem, status_code=status.HTTP_201_CREATED)
async def add_wishlist_item(pet_id: int, item: WishlistCreate):
    """Fügt der Wunschliste eines Tieres ein Geschenk hinzu."""
    for pet in pets_db:
        if pet["id"] == pet_id:
            new_item_id = max([w["id"] for w in pet["wishlist"]], default=pet_id * 100) + 1
            new_item = {
                "id": new_item_id,
                "item_name": item.item_name,
                "category": item.category,
                "status": "offen"
            }
            pet["wishlist"].append(new_item)
            return new_item
    raise HTTPException(status_code=404, detail="Haustier nicht gefunden")

@app.patch("/pets/{pet_id}/wishlist/{item_id}/buy", response_model=WishlistItem)
async def mark_wishlist_item_as_bought(pet_id: int, item_id: int):
    """Markiert ein Wunschlisten-Geschenk als 'gekauft'."""
    for pet in pets_db:
        if pet["id"] == pet_id:
            for item in pet["wishlist"]:
                if item["id"] == item_id:
                    item["status"] = "gekauft"
                    return item
            raise HTTPException(status_code=404, detail="Wunschlisten-Eintrag nicht gefunden")
    raise HTTPException(status_code=404, detail="Haustier nicht gefunden")