import os
import csv
import sqlite3
import hashlib
import glob

def clean_currency(value):
    if not value:
        return 0.0
    s = str(value).strip().replace('R$', '').replace('R$ ', '').strip()
    s = s.replace('.', '').replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return 0.0

def compute_row_hash(public_code, city, state, typology, estimated_vgv, min_bid):
    hash_input = f"{public_code}|{city}|{state}|{typology}|{estimated_vgv}|{min_bid}"
    return hashlib.md5(hash_input.encode('utf-8')).hexdigest()

print("Iniciando script import_assets.py...")
db_path = '../assets.db'
print(f"Conectando ao banco de dados: {os.path.abspath(db_path)}")
conn = sqlite3.connect(db_path)
cur = conn.cursor()
print("Criando tabela 'assets' se não existir...")
cur.execute("""
CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    public_code TEXT UNIQUE NOT NULL,
    city TEXT,
    state TEXT,
    typology TEXT,
    estimated_vgv REAL,
    min_bid REAL,
    row_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

csv_files = glob.glob('*.csv')
print(f"Encontrados {len(csv_files)} arquivos CSV: {', '.join([os.path.basename(f) for f in csv_files])}")

total_rows = 0
for filename in csv_files:
    print(f"\nProcessando arquivo: {os.path.basename(filename)}")
    row_count = 0
    try:
        with open(filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(reader, 1):
                public_code = row.get('processo', '').strip()
                if not public_code:
                    continue
                city = row.get('cidade', '').strip()
                state = row.get('estado', '').strip()
                typology = row.get('tipo', '').strip()
                estimated_vgv = clean_currency(row.get('avaliação'))
                min_bid = clean_currency(row.get('arremate'))
                row_hash = compute_row_hash(public_code, city, state, typology, estimated_vgv, min_bid)
                cur.execute("""
                    INSERT OR REPLACE INTO assets 
                    (public_code, city, state, typology, estimated_vgv, min_bid, row_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (public_code, city, state, typology, estimated_vgv, min_bid, row_hash))
                row_count += 1
                if row_num % 100 == 0:
                    print(f"  Processadas {row_num} linhas de {filename}...")
        print(f"Concluído {os.path.basename(filename)}: {row_count} linhas importadas/atualizadas.")
        total_rows += row_count
    except Exception as e:
        print(f"Erro ao processar {filename}: {e}")

conn.commit()
print(f"\nImportação concluída! Total de {total_rows} linhas processadas.")
print(f"Banco salvo em: {os.path.abspath(db_path)}")
cur.execute("SELECT COUNT(*) FROM assets")
count = cur.fetchone()[0]
print(f"Total de registros na tabela assets: {count}")
conn.close()
print("Script finalizado.")