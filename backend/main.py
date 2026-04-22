from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sys

# 1. Ajuste de Path para garantir que a Vercel encontre os módulos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Importação dos roteadores e do banco
from app.routes import wellness, oportunidades
from app.models.database import create_tables

# 2. Carrega variáveis de ambiente
load_dotenv()

# 3. Inicializa a aplicação
app = FastAPI(
    title="Prata Real Estate - Advocacia Hub",
    description="Mesa de Originação e Gestão de Ativos Distressed",
    version="0.1.0"
)

# 4. Configuração de CORS Blindada
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pratarealestate.com.br", 
        "https://www.pratarealestate.com.br",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Criar as tabelas ao iniciar
try:
    # Garantimos que o banco seja criado/lido no local correto
    create_tables()
except Exception as e:
    print(f"Aviso: Erro na base de dados: {e}")

# 6. Registro das Rotas
app.include_router(wellness.router)
app.include_router(oportunidades.router)

# 7. Rotas de Status
@app.get("/")
def read_root():
    return {
        "message": "Prata Real Estate API está rodando!",
        "status": "online",
        "version": "0.1.0",
        "environment": "production" if os.getenv("VERCEL") else "development"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 8. Execução Local
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)