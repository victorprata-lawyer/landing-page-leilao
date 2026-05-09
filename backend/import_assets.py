import os
import sqlite3
import csv
import glob

def clean_money(s):
    if not s:
        return 0.0
    s = str(s).strip().replace('R$ ', '').replace('R$', '').replace('.', '').replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return 0.0

DB_PATH = '../assets.db'

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS assets
             (public_code TEXT PRIMARY KEY,
              city TEXT,
              state TEXT,
              typology TEXT,
              estimated_vgv REAL,
              min_bid REAL)''')

csv_files = glob.glob('*.csv')

for file_path in csv_files:
    print(f"Processing {file_path}...")
    with open(file_path, 'r', encoding='utf-8-sig', newline='', errors='ignore') as f:
        try:
            sample = f.read(1024)
            dialect = csv.Sniffer().sniff(sample)
            f.seek(0)
        except:
            dialect = csv.excel
            f.seek(0)
        reader = csv.reader(f, dialect)
        headers = next(reader)
        print(f"Headers: {headers}")
        num_cols = len(headers)
        count = 0
        for row_num, row in enumerate(reader, 2):
            if len(row) > num_cols:
                row = row[:num_cols]
            row = [field.strip() for field in row]
            if len(row) < 6:
                continue  # Skip invalid rows
            try:
                public_code = row[0]
                if not public_code:
                    continue
                city = row[1]
                state = row[2]
                typology = row[3]
                estimated_vgv = clean_money(row[4])
                min_bid = clean_money(row[5])
                c.execute('''INSERT OR IGNORE INTO assets
                             (public_code, city, state, typology, estimated_vgv, min_bid)
                             VALUES (?, ?, ?, ?, ?, ?)''',
                          (public_code, city, state, typology, estimated_vgv, min_bid))
                count += 1
            except Exception as e:
                print(f"Error on row {row_num} of {file_path}: {e}")
                continue
        print(f"Inserted/updated {count} assets from {file_path}")

conn.commit()
conn.close()
print("Import complete!")