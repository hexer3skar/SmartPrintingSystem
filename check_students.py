import sqlite3

# الاتصال بقاعدة البيانات
conn = sqlite3.connect('admin_system.db')
cursor = conn.cursor()

# جلب جميع بيانات الطلاب
cursor.execute("SELECT * FROM students")
students = cursor.fetchall()

# التحقق من وجود طلاب
if students:
    print("قائمة الطلاب في قاعدة البيانات:")
    for student in students:
        print(f"رقم الجلوس: {student[0]}, الاسم: {student[1]}, الرصيد: {student[2]} جنيه")
else:
    print("⚠ لا يوجد طلاب مسجلين في قاعدة البيانات.")

conn.close()