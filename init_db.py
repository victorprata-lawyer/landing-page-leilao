import sqlite3
import os

# Define onde o banco será criado (na raiz do seu projeto)
db_path = os.path.join(os.getcwd(), "assets.db")

def criar_banco_direto():
    try:
        # Conecta (ou cria) o arquivo assets.db
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Criando a tabela de ativos (Mesa de Originação)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                internal_code TEXT NOT NULL,
                public_code TEXT NOT NULL,
                process_number TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                typology TEXT NOT NULL,
                estimated_vgv REAL NOT NULL,
                leilao_percent REAL NOT NULL,
                is_public BOOLEAN DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Sucesso! Banco de dados criado em: {db_path}")
    except Exception as e:
        print(f"❌ Erro ao criar banco: {e}")

if __name__ == "__main__":
    criar_banco_direto()