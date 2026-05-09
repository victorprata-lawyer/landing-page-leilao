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
    # Provide defaults for missing fields
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

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets.db")

# Example data - replace with real data from your source (e.g., API or JSON file)
data = [
    {
        "Public Code": "PR001",
        "Cidade": "São Paulo",
        "Estado": "SP",
        "Tipo": "Apartamento",
        "Avaliação": "1.234.567,89",
        "Arremate": "987.654,32"
    },
    {
        "public_code": "PR002",
        "cidade": "Rio de Janeiro",
        "estado": "RJ",
        "tipo": "Casa",
        "avaliacao": "500.000,00",
        "arremate": "400.000,00"
    }
    # Add more rows here or load from file: data = json.load(open('raw_data.json'))
]

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
    for row in data:
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
            cleaned['c['estado'],
            cleaned['tipo'],
            cleaned['avaliacao'],
            cleaned['arremate']
        ))
        count += 1

    conn.commit()

abs_db_path = os.path.abspath(DB_PATH)
print(f"Database saved at: {abs_db_path}")
print(f"Processed {count} rows. Table 'assets' is now populated.")