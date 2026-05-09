import os
import sqlite3
import hashlib

def limpar_chave(chave):
    if not chave:
        return ''
    chave = str(chave).strip().lower()
    chave = chave.replace(' ', '_').replace('-', '_').replace('/', '_')
    return chave

def limpar_valor_numerico(valor):
    if valor is None or valor == '':
        return 0.0
    if isinstance(valor, (int, float)):
        return float(valor)
    s = str(valor).strip()
    s = s.replace('.', '').replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return 0.0

def process_row(row):
    cleaned = {}
    for k, v in row.items():
        clean_k = limpar_chave(k)
        if clean_k == 'public_code':
            cleaned['public_code'] = str(v).strip() if v else ''
        elif clean_k == 'cidade':
            cleaned['cidade'] = str(v).strip() if v else ''
        elif clean_k == 'estado':
            cleaned['estado'] = str(v).strip() if v else ''
        elif clean_k == 'tipo':
            cleaned['tipo'] = str(v).strip() if v else ''
        elif clean_k in ['avaliacao', 'arremate']:
            cleaned[clean_k] = limpar_valor_numerico(v)
    
    defaults = {
        'public_code': '',
        'cidade': '',
        'estado': '',
        'tipo': '',
        'avaliacao': 0.0,
        'arremate': 0.0
    }
    for field, default in defaults.items():
        cleaned.setdefault(field, default)
    return cleaned

# Path to database in project root (../assets.db from script directory)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets.db")

# Example data (replace with your CSV reading logic if necessary)
data = [
    {
        "public_code": "PR001",
        "cidade": "São Paulo",
        "estado": "SP",
        "tipo": "Apartamento",
        "avaliacao": "1.234.567,89",
        "arremate": "987.654,32"
    }
]

def executar_importacao(lista_dados):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS assets (
                row_hash TEXT PRIMARY KEY,
                public_code TEXT,
                cidade TEXT,
                estado TEXT,
                tipo TEXT,
                avaliacao REAL,
                arremate REAL
            )
        """)

        count = 0
        for row in lista_dados:
            cleaned = process_row(row)
            fields_for_hash = [
                str(cleaned['public_code']),
                str(cleaned['cidade']),
                str(cleaned['estado']),
                str(cleaned['tipo']),
                str(cleaned['avaliacao']),
                str(cleaned['arremate'])
            ]
            row_hash = hashlib.md5('||'.join(fields_for_hash).encode('utf-8')).hexdigest()

            conn.execute("""
                INSERT OR REPLACE INTO assets
                (row_hash, public_code, cidade, estado, tipo, avaliacao, arremate)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                row_hash,
                cleaned['public_code'],
                cleaned['cidade'],
                cleaned['estado'],
                cleaned['tipo'],
                cleaned['avaliacao'],
                cleaned['arremate']
            ))
            count += 1
        conn.commit()
    print(f"Banco atualizado em: {os.path.abspath(DB_PATH)}")
    print(f"Processados {count} ativos.")

if __name__ == "__main__":
    executar_importacao(data)
