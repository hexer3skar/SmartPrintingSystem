import sqlite3
import bcrypt

conn = sqlite3.connect(r'C:\Users\3skar\new project\students.db')
cursor = conn.cursor()

# ✅ إنشاء جدول الإداريين إذا لم يكن موجودًا
cursor.execute('''
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# ✅ إضافة مدير افتراضي (admin) إذا لم يكن موجودًا
default_admin_username = "admin"
default_admin_password = "1234"

cursor.execute("SELECT * FROM admins WHERE username = ?", (default_admin_username,))
if not cursor.fetchone():
    hashed_password = bcrypt.hashpw(default_admin_password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", (default_admin_username, hashed_password))
    conn.commit()
    print("✅ تم إنشاء حساب المدير الافتراضي بنجاح!")

conn.close()