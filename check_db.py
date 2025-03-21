import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("📌 الجداول الموجودة في قاعدة البيانات:")
for table in tables:
    print(f"- {table[0]}")

# التأكد من أن الطالب 2420792 موجود
cursor.execute("SELECT id, name, balance FROM students WHERE id = ?", ("2420792",))
student = cursor.fetchone()

if student:
    print(f"✅ الطالب موجود: رقم الجلوس: {student[0]}, الاسم: {student[1]}, الرصيد: {student[2]} جنيه")
else:
    print("⚠ الطالب 2420792 غير موجود في قاعدة البيانات!")

conn.close()
