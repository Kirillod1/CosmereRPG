from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, get_db

# Ta linijka automatycznie stworzy plik bazy danych i tabele na podstawie modeli z models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cosmere RPG API")

@app.get("/")
def powitanie():
    return {"Wiadomość": "Podróż przed celem! Witaj w Cosmere RPG API."}

# Endpoint 1: Tworzenie nowej postaci
@app.post("/characters/")
def stworz_postac(character_data: dict, db: Session = Depends(get_db)):
    # Tworzymy obiekt nowej postaci na podstawie danych przesłanych przez użytkownika
    nowa_postac = models.Character(
        name=character_data.get("name"),
        origin=character_data.get("origin", "Human"),
        starting_path=character_data.get("starting_path"),
        level=character_data.get("level", 1),
        purpose=character_data.get("purpose"),
        obstacle=character_data.get("obstacle"),
        strength=character_data.get("strength", 0),
        speed=character_data.get("speed", 0),
        intelligence=character_data.get("intelligence", 0),
        willpower=character_data.get("willpower", 0),
        awareness=character_data.get("awareness", 0),
        presence=character_data.get("presence", 0),
        skills=character_data.get("skills", {}),
        equipment=character_data.get("equipment", []),
        magic_and_resources=character_data.get("magic_and_resources", {})
    )
    
    # Zapisujemy do bazy danych
    db.add(nowa_postac)
    db.commit()
    db.refresh(nowa_postac)
    return nowa_postac

# Endpoint 2: Pobieranie wszystkich postaci z bazy
@app.get("/characters/")
def pobierz_postacie(db: Session = Depends(get_db)):
    postacie = db.query(models.Character).all()
    return postacie