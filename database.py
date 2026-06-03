
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ścieżka do naszej lokalnej bazy danych SQLite (plik cosmere_rpg.db w folderze projektu)
SQLALCHEMY_DATABASE_URL = "sqlite:///./cosmere_rpg.db"

# create_engine informuje SQLAlchemy o rodzaju bazy (connect_args jest potrzebne tylko dla SQLite)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Tworzymy fabrykę sesji – za jej pomocą będziemy dodawać i pobierać postacie z bazy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Funkcja pomocnicza, którą FastAPI wykorzysta do bezpiecznego otwierania i zamykania połączenia z bazą
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()