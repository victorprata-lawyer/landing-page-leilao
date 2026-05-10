import sys
import os

# Adiciona a pasta 'backend' ao caminho de busca do Python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(BASE_DIR, 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Importa usando o caminho completo dentro da estrutura do app
try:
    from app.models.database import engine
    with engine.connect() as conn:
        print("✅ Conexão com assets.db bem-sucedida!")
        print(f"📍 Banco localizado em: {engine.url}")
except ImportError as e:
    print(f"❌ Erro de Importação: {e}")
except Exception as e:
    print(f"⚠️ Erro de Conexão: {e}")