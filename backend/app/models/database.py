from pathlib import Path
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Localiza a raiz do projeto (advocacia-hub) subindo 3 níveis
root_path = Path(__file__).resolve().parents[3]

DATABASE_URL = os.getenv("DATABASE_URL")
# Garante que o nome do arquivo seja assets.db
DATABASE_PATH = root_path / "assets.db"

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
else:
    # Conexão SQLite apontando para a raiz
    engine = create_engine(
        f"sqlite:///{DATABASE_PATH}",
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Gera uma sessão do banco para dependência no FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Cria todas as tabelas, evitando importação circular."""
    from app.models.models import Base
    Base.metadata.create_all(bind=engine)