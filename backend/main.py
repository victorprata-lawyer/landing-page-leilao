# Configuração inicial do path para garantir que imports locais funcionem corretamente
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Carrega variáveis de ambiente do arquivo .env
from dotenv import load_dotenv
load_dotenv()

# Imports do FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Imports locais do projeto (agora funcionam com path configurado)
from app.routes import wellness, oportunidades
from app.models.database import create_tables
from integrations.zapsign import router as zapsign_router

# Cria a aplicação FastAPI
app = FastAPI(
    title="Backend API",
    version="1.0.0",
    description="API backend principal"
)

# Configuração do CORS (preservada)
allow_origins = [
    "http://localhost:3000",
    "https://your-frontend.vercel.app",  # Ajuste conforme o frontend
    "*"  # Em produção, especifique domínios exatos
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria as tabelas do banco apenas se não estiver no Vercel (preservado)
if os.environ.get("VERCEL") != "1":
    create_tables()

# Inclui as rotas (preservado, sem alteração de nomes ou prefixos)
app.include_router(wellness.router)
app.include_router(oportunidades.router, prefix="/api")
app.include_router(zapsign_router)

# Rota raiz (preservada)
@app.get("/")
def root():
    return {"message": "Backend rodando!"}

# Rota de health check (preservada)
@app.get("/health")
def health():
    return {"status": "ok"}

# Bloco uvicorn para execução local (preservado)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)