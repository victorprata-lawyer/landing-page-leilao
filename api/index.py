import sys
import os

# Adiciona o diretório backend ao sys.path (compatível com Vercel)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Importa o app FastAPI do main.py
from main import app

# Adaptador Mangum para runtime serverless da Vercel
from mangum import Mangum

mangum_handler = Mangum(app)

# Handler obrigatório para Vercel Python serverless functions
def handler(event, context):
    """Endpoint principal para chamadas API na Vercel."""
    return mangum_handler(event, context)
