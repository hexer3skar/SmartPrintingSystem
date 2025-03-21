import sqlite3

db = sqlite3.connect("printing_system.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rfid TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    balance REAL NOT NULL DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS print_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    document_name TEXT,
    pages INTEGER,
    cost REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
""")

db.commit()
db.close()

print("The database is ready!")