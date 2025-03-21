import sqlite3

conn = sqlite3.connect('admin_system.db')
cursor = conn.cursor()

# بيانات الطلاب الجديدة
students_data = [
    ("12345", "Ahmed Ali", 50.0),
    ("67890", "Sara Mohamed", 30.0),
    ("2420792", "Aly Eldean Mohamed", 100.0)  # إضافة الطالب المطلوب
]

for student in students_data:
    student_id, name, balance = student

    # التحقق مما إذا كان الطالب موجودًا بالفعل
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    existing_student = cursor.fetchone()

    if existing_student:
        print(f"⚠ الطالب برقم {student_id} موجود بالفعل!")
    else:
        cursor.execute("INSERT INTO students (student_id, name, balance) VALUES (?, ?, ?)", student)
        print(f"✅ تم إضافة الطالب {name} برقم {student_id} بنجاح!")

# حفظ التغييرات وإغلاق الاتصال
conn.commit()
conn.close()
