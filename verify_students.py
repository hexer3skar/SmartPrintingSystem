import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# جلب جميع بيانات الطلاب والتأكد من رقم الجلوس
cursor.execute("SELECT * FROM students")
students = cursor.fetchall()

if students:
    print("📌 قائمة الطلاب في قاعدة البيانات:")
    for student in students:
        print(f"🔹 ID: {student[0]}, الاسم: {student[1]}, الرصيد: {student[2]} جنيه")
else:
    print("⚠ لا يوجد طلاب مسجلين في قاعدة البيانات!")

conn.close()