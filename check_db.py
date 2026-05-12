import sqlite3

try:
    conn = sqlite3.connect('assets.db')
    cursor = conn.cursor()

    # List all tables (excluding sqlite internal tables)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]

    if not tables:
        print("No tables found in the database.")
    else:
        print(f"Found {len(tables)} tables:")
        for table in tables:
            # Count records in the table
            cursor.execute(f"SELECT COUNT(*) FROM [{table}];")
            count = cursor.fetchone()[0]
            print(f"  - {table}: {count} records")

            # If 'oportunidades' table, list columns
            if table == 'oportunidades':
                cursor.execute(f"PRAGMA table_info([{table}]);")
                columns = [row[1] for row in cursor.fetchall()]
                print(f"    Columns: {', '.join(columns)}")

    conn.close()
    print("Diagnosis complete.")

except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")