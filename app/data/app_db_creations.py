import sqlite3

# Créer une nouvelle base de données SQLite app.db
db_path = "/mnt/data/app.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Création d'une table exemple "User"
cursor.execute("""
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL
);
""")

# Sauvegarde et fermeture
conn.commit()
conn.close()

# Retourner le fichier app.db
db_path
