
import sqlite3
import os

db_path = "murim.db"

def migrate():
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("Adding 'family' column...")
        cursor.execute("ALTER TABLE characters ADD COLUMN family TEXT")
    except sqlite3.OperationalError as e:
        print(f"Could not add 'family': {e}")

    try:
        print("Adding 'alliances' column...")
        cursor.execute("ALTER TABLE characters ADD COLUMN alliances TEXT")
    except sqlite3.OperationalError as e:
        print(f"Could not add 'alliances': {e}")

    try:
        print("Adding 'abilities' column...")
        cursor.execute("ALTER TABLE characters ADD COLUMN abilities TEXT")
    except sqlite3.OperationalError as e:
        print(f"Could not add 'abilities': {e}")

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
