import sqlite3

# أسماء قواعد البيانات لديك
databases = ["data_base.db", "printing_system.db", "students.db"]

for db in databases:
    try:
        print(f"\n🔍 التحقق من قاعدة البيانات: {db}")
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        
        # عرض أسماء الجداول داخل قاعدة البيانات
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if tables:
            print(f"📌 الجداول الموجودة في {db}: {tables}")
            
            # التحقق مما إذا كان هناك جدول باسم "students"
            if ('students',) in tables:
                cursor.execute("SELECT * FROM students")
                students = cursor.fetchall()
                if students:
                    print(f"✅ يوجد طلاب في {db}:")
                    for student in students:
                        print(f"رقم الجلوس: {student[0]}, الاسم: {student[1]}, الرصيد: {student[2]} جنيه")
                else:
                    print(f"⚠ لا يوجد طلاب في {db}")
        else:
            print(f"⚠ لا يوجد جداول في {db}")

        conn.close()
    except Exception as e:
        print(f"❌ خطأ في {db}: {e}")