import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# جلب أسماء الأعمدة في جدول students
cursor.execute("PRAGMA table_info(students);")
columns = cursor.fetchall()

if columns:
    print("📌 الأعمدة الموجودة في جدول students:")
    for column in columns:
        print(f"- {column[1]}")
else:
    print("❌ خطأ: لا يوجد جدول students في قاعدة البيانات!")

conn.close()