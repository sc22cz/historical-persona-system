import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "historical.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS figures (
            id        INTEGER PRIMARY KEY,
            name      TEXT NOT NULL,
            era       INTEGER,
            period    TEXT,
            source    TEXT,
            raw_text  TEXT
        );

        CREATE TABLE IF NOT EXISTS profiles (
            id          INTEGER PRIMARY KEY,
            figure_id   INTEGER REFERENCES figures(id),
            vector      TEXT,
            confidence  TEXT,
            evidence    TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS similarities (
            id          INTEGER PRIMARY KEY,
            figure_a    INTEGER REFERENCES figures(id),
            figure_b    INTEGER REFERENCES figures(id),
            score       REAL,
            computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    conn.close()
    print("Database initialised successfully.")

if __name__ == "__main__":
    init_db()