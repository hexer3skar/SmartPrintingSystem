import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rfid TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        balance REAL NOT NULL
    )
""")

conn.commit()
conn.close()

print("✅the schedule has been created successfully!")