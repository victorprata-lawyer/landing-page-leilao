import sqlite3
import os
import json

db_path = '../assets.db'
print(f"Checking database: {db_path}")

if not os.path.exists(db_path):
    print("ERROR: Database file not found.")
    exit(1)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Check if table 'assets' exists
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='assets';")
if not cur.fetchone():
    print("ERROR: Table 'assets' does not exist.")
    conn.close()
    exit(1)

print("✓ Table 'assets' exists.")

# List columns using PRAGMA table_info
cur.execute("PRAGMA table_info(assets);")
columns_info = cur.fetchall()
column_names = [col[1] for col in columns_info]

print("\nColumns in 'assets':")
for col in column_names:
    print(f"  - {col}")

expected = ['estimated_vgv', 'public_code']
missing = [e for e in expected if e not in column_names]
if missing:
    print(f"WARNING: Missing expected columns: {missing}")
else:
    print("✓ All expected columns present.")

# Fetch first 5 records
print("\nFirst 5 raw records:")
cur.execute("SELECT * FROM assets LIMIT 5")
rows = cur.fetchall()
headers = [description[0] for description in cur.description]

print("Headers:", headers)

for i, row in enumerate(rows, 1):
    print(f"Row {i}: {dict(zip(headers, row))}")

# Simulate API /api/oportunidades response
print("\nSimulated /api/oportunidades response (first 5):")
valid_vgv = False
valid_public = False
api_data = []

for row in rows:
    data = dict(zip(headers, row))
    api_data.append(data)
    if 'estimated_vgv' in data:
        vgv = data['estimated_vgv']
        if vgv is not None and vgv > 0:
            valid_vgv = True
    if 'public_code' in data:
        pc = data['public_code']
        if pc is not None and pc > 0:
            valid_public = True

for data in api_data:
    print(json.dumps(data, indent=2, default=str))

if valid_vgv:
    print("✓ 'estimated_vgv' has valid values (>0) in samples.")
else:
    print("✗ 'estimated_vgv' missing or invalid (<=0/None) in samples.")

if valid_public:
    print("✓ 'public_code' has valid values (>0) in samples.")
else:
    print("✗ 'public_code' missing or invalid (<=0/None) in samples.")

print("\nDiagnostic complete.")

conn.close()
