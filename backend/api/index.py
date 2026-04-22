import sys
import os

# Adiciona a pasta raiz do backend ao path para que o Python encontre seus modelos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# A Vercel precisa que o objeto da aplicação seja exportado como 'app'
handle = app