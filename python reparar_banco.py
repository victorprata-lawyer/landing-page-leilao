import sqlite3

def forcar_reparo():
    conn = sqlite3.connect("assets.db")
    cursor = conn.cursor()
    
    print("🛠️ Forçando criação da coluna faltante...")
    
    try:
        # Adiciona a coluna sem a restrição UNIQUE para evitar o erro do SQLite
        cursor.execute("ALTER TABLE assets ADD COLUMN codigo_oportunidade TEXT")
        print("✅ Coluna 'codigo_oportunidade' adicionada com sucesso.")
    except sqlite3.OperationalError:
        print("ℹ️ A coluna já existe ou houve um erro de permissão.")
    except Exception as e:
        print(f"❌ Erro: {e}")

    conn.commit()
    conn.close()
    print("🚀 Operação finalizada.")

if __name__ == "__main__":
    forcar_reparo()