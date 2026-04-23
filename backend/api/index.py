import sys
import os
from pathlib import Path

# Correção mínima: adiciona /backend ao sys.path para imports funcionarem
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from main import app  # Importa o app do backend/main.py

# Para deploy serverless (Vercel, etc.) com FastAPI via Mangum
try:
    from mangum import Mangum
    handler = Mangum(app)
except ImportError:
    handler = None

# Para teste local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Handler para serverless
def handler(event, context):
    if handler:
        return handler(event, context)
    raise Exception("Mangum não instalado. Instale com: pip install mangum")

Nota curta:
- O import em backend/app/routes/oportunidades.py pode continuar usando app.models.database
- O main.py pode ficar como está
- Primeiro teste: abra /api/oportunidades/ no navegador
