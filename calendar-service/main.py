from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Calendar Service")

class BirthdayItem(BaseModel):
    id: int
    name: str
    species: str
    date: str  # Format: "YYYY-MM-DD" oder "DD.MM."
    age: int

# Simulierte Kalender-Daten
calendar_db = [
    {"id": 1, "name": "Cheesy", "species": "Hund", "date": "15.05.2021", "age": 5},
    {"id": 2, "name": "Almi", "species": "Katze", "date": "22.08.2022", "age": 4}
]

@app.get("/birthdays", response_model=List[BirthdayItem])
async def get_birthdays():
    """Gibt alle Tiergeburtstage und Termine zurück."""
    return calendar_db

@app.post("/birthdays", response_model=BirthdayItem, status_code=status.HTTP_201_CREATED)
async def add_birthday(item: BirthdayItem):
    """Fügt einen neuen Geburtstag zum Kalender hinzu."""
    calendar_db.append(item.dict())
    return item