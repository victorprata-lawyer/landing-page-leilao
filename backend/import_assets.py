import sqlite3
import csv
import os
import unicodedata
import re
import hashlib
from datetime import datetime, timedelta

#--- AJUSTE DE CAMINHO DINÂMICO ---
# Ele identifica a pasta onde o script está e aponta para o assets.db no mesmo local
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "assets.db")

def limpar_chave(chave):
    nfkd = unicodedata.normalize('NFKD', chave)
    limpa = "".join([c for c in nfkd if not unicodedata.combining(c)])
    return limpa.lower().strip().replace(" ", "_").replace("%", "").replace("$", "")

def limpar_valor_numerico(val):
    if not val or str(val).strip() in ['-', '', 'N/D', 'N/A', 'nan']:
        return 0.0
    texto = str(val).strip().upper()
    if 'E' in texto and any(char.isdigit() for char in texto):
        try: return float(texto)
        except: pass
    texto = re.sub(r'[^\d.,]', '', texto)
    if not texto: return 0.0
    if ',' in texto and '.' in texto:
        texto = texto.replace('.', '').replace(',', '.')
    elif ',' in texto:
        texto = texto.replace(',', '.')
    elif texto.count('.') > 1:
        partes = texto.split('.')
        texto = "".join(partes[:-1]) + "." + partes[-1]
    try: return float(texto)
    except: return 0.0

def garantir_tabela(cursor):
    """Cria a tabela se não existir, SEM apagar os dados anteriores."""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            internal_code TEXT,
            public_code TEXT,
            process_number TEXT, 
            city TEXT,
            state TEXT,
            typology TEXT,
            estimated_vgv REAL,
            min_bid REAL,
            discount_percentage REAL,
            is_public INTEGER,
            metragem REAL,
            row_hash TEXT UNIQUE -- Chave para evitar duplicidade de linha
        )
    ''')

def importar_planilha():
    arquivos = [f for f in os.listdir('.') if f.endswith('.csv')]
    if not arquivos:
        print("❌ Nenhum arquivo .csv encontrado.")
        return

    print("\n--- 📂 Seleção de Planilha (Acumulativo) ---")
    for i, arq in enumerate(arquivos):
        print(f"[{i}] {arq}")
    
    try:
        escolha = int(input("\n👉 Selecione a planilha para ADICIONAR ao banco: "))
        csv_path = arquivos[escolha]
    except: return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    garantir_tabela(cursor)
    
    hoje = datetime.now()
    limite_passado = hoje - timedelta(days=60)
    data_ref = hoje.strftime("%m%y")
    
    novos = 0
    duplicados = 0

    with open(csv_path, mode='r', encoding='utf-8-sig') as f:
        content = f.read(2048)
        f.seek(0)
        delimiter = ';' if ';' in content else ','
        reader = csv.DictReader(f, delimiter=delimiter)
        reader.fieldnames = [limpar_chave(h) for h in reader.fieldnames]
        
        print(f"🚀 Minerando dados de {csv_path}...")

        for index, row in enumerate(reader):
            try:
                # 1. Identidade única da linha para evitar duplicar o mesmo imóvel da mesma planilha
                linha_str = "".join(str(v) for v in row.values())
                row_hash = hashlib.md5(linha_str.encode()).hexdigest()

                # 2. Janela de 60 dias
                data_str = row.get('data_leilao', row.get('leilao', '')).strip()
                is_public = 1
                if data_str:
                    try:
                        data_leilao = datetime.strptime(data_str, "%d/%m/%Y")
                        if data_leilao < limite_passado:
                            is_public = 0
                    except: pass

                # 3. Valores
                vgv = limpar_valor_numerico(row.get('avaliacao', '0'))
                p_raw = limpar_valor_numerico(row.get('leilao', row.get('_leilao', '50')))
                percentual = p_raw if p_raw > 1 else p_raw * 100
                min_bid = vgv * (percentual / 100)
                discount = 100 - percentual

                processo = row.get('processo', f"SN-{index}").strip()
                cidade = row.get('cidade', 'N/D').strip()
                estado = row.get('estado', 'N/D').strip()
                tipo = row.get('tipo', 'N/D').strip()
                metragem = limpar_valor_numerico(row.get('metragem', '0'))
                
                public_code = f"OP-{cidade.upper().replace(' ', '')}-{data_ref}-{index+1:03d}"
                
                dados = (
                    f"PR-{datetime.now().year}-{index+1:03d}",
                    public_code, processo, cidade, estado, tipo, 
                    vgv, min_bid, discount, is_public, metragem, row_hash
                )

                # INSERT OR IGNORE: Se o row_hash já existir, ele pula (não duplica nem apaga)
                cursor.execute('''
                    INSERT OR IGNORE INTO assets (
                        internal_code, public_code, process_number, city, state, 
                        typology, estimated_vgv, min_bid, discount_percentage, is_public, metragem, row_hash
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                ''', dados)
                
                if cursor.rowcount > 0:
                    novos += 1
                else:
                    duplicados += 1
            except: pass

    conn.commit()
    conn.close()
    print(f"\n✅ IMPORTAÇÃO CONCLUÍDA")
    print(f"💎 Novos ativos minerados: {novos}")
    print(f"🛡️ Itens já existentes (pulados): {duplicados}")

if __name__ == "__main__":
    importar_planilha()