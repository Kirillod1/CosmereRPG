
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

# To jest baza, z której będą dziedziczyć wszystkie nasze tabele
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="player") # Domyślnie każdy jest graczem. Mistrz Gry to będzie np. "gm"

class Character(Base):
    __tablename__ = "characters"

    # 1. Identyfikacja i podstawy
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    origin = Column(String, default="Human")
    starting_path = Column(String, nullable=True)
    level = Column(Integer, default=1)

    # 2. Fabuła
    purpose = Column(String, nullable=True)
    obstacle = Column(String, nullable=True)

    # 3. Atrybuty (sztywne kolumny ułatwią nam później matematykę przy rzutach kośćmi)
    strength = Column(Integer, default=0)
    speed = Column(Integer, default=0)
    intelligence = Column(Integer, default=0)
    willpower = Column(Integer, default=0)
    awareness = Column(Integer, default=0)
    presence = Column(Integer, default=0)

    # 4. Elastyczne worki na dane (Typ JSON)
    # Tu będziemy trzymać rzeczy, które będą się często zmieniać podczas poprawek
    skills = Column(JSON, default={})
    equipment = Column(JSON, default=[])
    magic_and_resources = Column(JSON, default={})