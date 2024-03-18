import sqlite3
from config import Config

# Adjusting DATABASE_URI extraction to match your setup
DATABASE_URI = Config.DATABASE_URI.split("///")[-1]

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URI)
    conn.row_factory = sqlite3.Row
    return conn

def create_user_table():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE,
                password_hash TEXT NOT NULL,
                role_id INTEGER
            );
        """)
        conn.commit()

def create_role_table():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
        """)
        conn.commit()

def init_db():
    """Initializes the database by creating necessary tables."""
    create_user_table()
    create_role_table()
    # Add more table creation functions here as needed

