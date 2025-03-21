import sqlite3

# الاتصال بقاعدة البيانات
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# جلب البيانات من الجدول
cursor.execute("SELECT * FROM students")
students = cursor.fetchall()

# طباعة البيانات
print("\n📌 البيانات الموجودة في الجدول:")
for student in students:
    print(student)

# إغلاق الاتصال
conn.close()