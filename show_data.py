import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()

if rows:
    print("📋 stored student data:")
    for row in rows:
        print(row)
else:
    print("⚠ there is no data in the table!")

conn.close()