from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from urllib.parse import urlparse
import os

from app.models.models import Base

# Determina a URL do banco de dados com prioridade: DATABASE_URL -> DATABASE_PATH -> assets.db na raiz

database_url = os.getenv('DATABASE_URL')
db_path = None

if database_url:
    if database_url.startswith('sqlite://'):
        parsed = urlparse(database_url)
        file_path = parsed.path.lstrip('/')
        db_path = Path(file_path).resolve()
        if not db_path.exists():
            raise FileNotFoundError(f"Arquivo de banco não encontrado: {db_path}")
        print(f"Caminho final do banco: {db_path}")
    else:
        # Para outros bancos como PostgreSQL
        print(f"Usando DATABASE_URL: {database_url}")
        db_path = None
else:
    database_path = os.getenv('DATABASE_PATH')
    if database_path:
        db_path = Path(database_path).resolve()
        if not db_path.exists():
            raise FileNotFoundError(f"Arquivo de banco não encontrado: {db_path}")
        print(f"Caminho final do banco: {db_path}")
        database_url = f"sqlite:///{db_path}"
    else:
        # Fallback para assets.db na raiz do projeto advocacia-hub
        root_path = Path(__file__).resolve().parents[3]
        db_path = root_path / "assets.db"
        if not db_path.exists():
            raise FileNotFoundError(f"Arquivo de banco não encontrado: {db_path}")
        print(f"Caminho final do banco: {db_path}")
        database_url = f"sqlite:///{db_path}"

# Cria o motor do banco de dados
is_sqlite = database_url and database_url.startswith('sqlite://')
connect_args = {"check_same_thread": False} if is_sqlite else {}
engine = create_engine(database_url, connect_args=connect_args)

def create_tables():
    """Cria todas as tabelas definidas nos models."""
    Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Gera uma sessão do banco para dependência no FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()