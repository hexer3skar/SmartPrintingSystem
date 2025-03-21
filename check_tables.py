import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# عرض جميع الجداول الموجودة في قاعدة البيانات
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

if tables:
    print("📌 الجداول الموجودة في قاعدة البيانات:")
    for table in tables:
        print(f"- {table[0]}")
else:
    print("⚠ لا توجد جداول في قاعدة البيانات!")

conn.close()