import sqlite3
import os

db_path = os.path.join("..", "assets.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(f"--- Verificando Banco: {os.path.abspath(db_path)} ---")

# 1. Verifica se a tabela existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()
print(f"Tabelas encontradas: {tabelas}")

# 2. Tenta contar os registros na tabela 'assets'
try:
    cursor.execute("SELECT COUNT(*) FROM assets")
    count = cursor.fetchone()[0]
    print(f"Total de registros na tabela 'assets': {count}")
    
    if count > 0:
        cursor.execute("SELECT public_code, city FROM assets LIMIT 1")
        print(f"Exemplo de dado: {cursor.fetchone()}")
except Exception as e:
    print(f"Erro ao ler tabela 'assets': {e}")

conn.close()