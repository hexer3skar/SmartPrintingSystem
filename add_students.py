import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# بيانات الطلاب التجريبية (يمكنك تغيير الأسماء والأرقام حسب الحاجة)
students_data = [
    ("2420792", "Ahmed Ali", 50.0),
    ("67890", "Sara Mohamed", 30.0),
    ("11223", "Aly Eldean Mohamed", 20.0)
]

for student in students_data:
    cursor.execute("INSERT OR IGNORE INTO students (id, name, balance) VALUES (?, ?, ?)", student)

conn.commit()
print("✅ تم إضافة الطلاب بنجاح!")
conn.close()