from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext # Narzędzie do szyfrowania
from pydantic import BaseModel # Do sprawdzania poprawności danych
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cosmere RPG API")

# Konfiguracja szyfrowania haseł (używamy algorytmu bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Schemat danych, których oczekujemy od formularza rejestracji
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# Schemat danych do logowania
class UserLogin(BaseModel):
    login: str  # Pozwolimy logować się przez email LUB nazwę użytkownika
    password: str

# Mówimy FastAPI, gdzie leżą nasze statyczne pliki (CSS, obrazki)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Zmieniony endpoint strony głównej - teraz zwraca nasz plik HTML!
@app.get("/")
def strona_glowna():
    return FileResponse("static/index.html")

# --- TUTAJ ZOSTAW PONIŻEJ SWOJE ENDPOINTY POST i GET do /characters/ ---

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

# --- SYSTEM KONT ---

@app.post("/register/")
def rejestracja(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Sprawdzamy, czy użytkownik o takiej nazwie lub emailu już istnieje
    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Użytkownik z taką nazwą lub emailem już istnieje.")

    # 2. Szyfrujemy hasło
    hashed_pw = pwd_context.hash(user.password)

    # 3. Tworzymy nowego użytkownika
    nowy_uzytkownik = models.User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_pw,
        role="player" # Każdy nowy to na start gracz
    )
    
    # 4. Zapisujemy w bazie
    db.add(nowy_uzytkownik)
    db.commit()
    db.refresh(nowy_uzytkownik)
    
    return {"message": "Konto zostało pomyślnie utworzone!", "username": nowy_uzytkownik.username}

@app.post("/login/")
def logowanie(user: UserLogin, db: Session = Depends(get_db)):
    # 1. Szukamy użytkownika po nazwie LUB emailu
    db_user = db.query(models.User).filter(
        (models.User.username == user.login) | (models.User.email == user.login)
    ).first()
    
    # 2. Jeśli nie ma takiego użytkownika...
    if not db_user:
        raise HTTPException(status_code=400, detail="Nieprawidłowy login lub hasło.")

    # 3. Sprawdzamy, czy wpisane hasło pasuje do tego z bazy
    if not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Nieprawidłowy login lub hasło.")

    # 4. Sukces! (Później dodamy tu prawdziwe "ciasteczka" sesji, na razie zwracamy info)
    return {
        "message": f"Witaj ponownie, {db_user.username}!", 
        "username": db_user.username,
        "role": db_user.role
    }