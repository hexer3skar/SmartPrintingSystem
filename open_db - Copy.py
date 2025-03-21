import sqlite3

# الاتصال بقاعدة البيانات الصحيحة
conn = sqlite3.connect('admin_data_base.db')
cursor = conn.cursor()

# التحقق من الجداول الموجودة في قاعدة البيانات
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("📌 الجداول الموجودة في قاعدة البيانات:", tables)

# جلب بيانات الطلاب
cursor.execute("SELECT * FROM students")
students = cursor.fetchall()

if students:
    print("📋 قائمة الطلاب:")
    for student in students:
        print(f"رقم الجلوس: {student[0]}, الاسم: {student[1]}, الرصيد: {student[2]} جنيه")
else:
    print("⚠ قاعدة البيانات لا تحتوي على أي طلاب.")

conn.close()