import os
import re
import csv
import sqlite3
import hashlib

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(parent_dir, 'assets.db')

def limpar_chave(key):
    key = str(key).strip()
    key = re.sub(r'\W+', '_', key)
    key = re.sub(r'_+', '_', key)
    key = key.strip('_')
    if not key:
        key = 'coluna'
    if key[0].isdigit():
        key = f'col_{key}'
    return key.lower()

def limpar_valor_numerico(valor):
    if not valor:
        return ''
    valor = str(valor).strip()
    valor = re.sub(r'[R$\s%]', '', valor)
    # Handle Brazilian format: 1.234,56 -> 1234.56
    if ',' in valor:
        parts = valor.split(',')
        if len(parts) == 2:
            integer_part = re.sub(r'\.', '', parts[0])
            decimal_part = parts[1][:10]  # limit decimals
            cleaned = f'{integer_part}.{decimal_part}'
            try:
                return str(float(cleaned))
            except ValueError:
                pass
    # Remove thousands separator
    valor = re.sub(r'\.', '', valor)
    valor = valor.replace(',', '.')
    try:
        return str(float(valor))
    except ValueError:
        return valor

def get_delimiter(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        sample = f.read(4096)
    sniffer = csv.Sniffer()
    try:
        dialect = sniffer.sniff(sample)
        return dialect.delimiter
    except:
        return ','

def compute_row_hash(row_dict):
    sorted_items = sorted(row_dict.items())
    data = '|'.join(f'{k}:{v}' for k, v in sorted_items)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def generate_codes(row_hash):
    h = hashlib.md5(row_hash.encode()).hexdigest()
    public_code = h[:8].upper()
    internal_code = h[8:16].upper()
    return public_code, internal_code

def import_csv(csv_file):
    table_name = limpar_chave(os.path.splitext(os.path.basename(csv_file))[0])
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    delimiter = get_delimiter(csv_file)

    # Read headers
    with open(csv_file, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter=delimiter)
        headers_raw = next(reader, [])
    headers = [limpar_chave(h) for h in headers_raw]

    # Additional columns
    all_cols = ['row_hash', 'public_code', 'internal_code'] + headers

    # Create table
    cols_def = ', '.join([f'"{c}" TEXT' for c in all_cols])
    create_sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({cols_def})'
    # Add UNIQUE constraint
    alter_sql = f'CREATE UNIQUE INDEX IF NOT EXISTS idx_{table_name}_row_hash ON "{table_name}" (row_hash)'
    cur.execute(create_sql)
    cur.execute(alter_sql)

    # Prepare insert
    col_names = ', '.join([f'"{c}"' for c in all_cols])
    placeholders = ', '.join(['?'] * len(all_cols))
    insert_sql = f'INSERT OR IGNORE INTO "{table_name}" ({col_names}) VALUES ({placeholders})'

    imported = 0
    skipped = 0

    # Read data
    with open(csv_file, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter=delimiter)
        next(reader)  # skip header
        for row_num, row in enumerate(reader, 1):
            if len(row) != len(headers):
                print(f"Linha {row_num} ignorada: número de colunas inconsistente ({len(row)} != {len(headers)})")
                continue
            row_dict = {headers[i]: limpar_valor_numerico(row[i]) for i in range(len(headers))}
            row_hash = compute_row_hash(row_dict)
            public_code, internal_code = generate_codes(row_hash)
            insert_data = (row_hash, public_code, internal_code) + tuple(row_dict.values())
            cur.execute(insert_sql, insert_data)
            if cur.rowcount > 0:
                imported += 1
            else:
                skipped += 1

    conn.commit()
    conn.close()
    print(f"Resumo para {csv_file}: {imported} linhas importadas, {skipped} ignoradas.")

def main():
    csv_files = [f for f in os.listdir('.') if f.lower().endswith('.csv')]
    if not csv_files:
        print("Nenhum arquivo CSV encontrado no diretório atual.")
        return

    while True:
        print("\n=== Menu de Importação de Assets ===")
        print("CSVs disponíveis:")
        for i, f in enumerate(csv_files, 1):
            print(f"{i}. {f}")
        print("0. Sair")
        choice = input("Escolha o número do CSV: ").strip()
        if choice == '0':
            break
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(csv_files):
                csv_file = csv_files[idx]
                confirm = input(f"Importar {csv_file}? (s/n): ").strip().lower()
                if confirm in ['s', 'sim', 'y', 'yes']:
                    print(f"Iniciando importação de {csv_file}...")
                    import_csv(csv_file)
                else:
                    print("Importação cancelada.")
            else:
                print("Escolha inválida.")
        except ValueError:
            print("Entrada inválida. Digite um número.")
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == '__main__':
    main()
