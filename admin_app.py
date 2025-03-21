import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import bcrypt
from plyer import notification

# ✅ إعدادات التصميم الأساسية
ctk.set_default_color_theme("blue")

# ✅ مسار قاعدة البيانات
DATABASE_PATH = r'C:\Users\LOQ\new project\students.db'

def get_db_connection():
    return sqlite3.connect(DATABASE_PATH, timeout=10)

# ✅ دالة فتح لوحة تحكم الإداري
def open_admin_dashboard(admin_username):
    dashboard = ctk.CTk()
    dashboard.title("Admin Dashboard")
    dashboard.geometry("700x600")
    dashboard.resizable(False, False)

    main_frame = ctk.CTkFrame(dashboard, width=650, height=550, corner_radius=15)
    main_frame.pack(pady=20)

    ctk.CTkLabel(main_frame, text=f"📊 Welcome, {admin_username}", font=("Arial", 18, "bold")).pack(pady=10)

    student_id_entry = ctk.CTkEntry(main_frame, placeholder_text="Student ID (RFID)", width=300)
    student_id_entry.pack(pady=5)

    amount_entry = ctk.CTkEntry(main_frame, placeholder_text="Amount to Add", width=300)
    amount_entry.pack(pady=5)

    # ✅ دالة تحديث الواجهة بشكل متكرر
    def update_ui():
        try:
            if dashboard.winfo_exists():
                global task_id
                task_id = dashboard.after(1000, update_ui)  # ✅ تحديث كل ثانية
        except Exception as e:
            print(f"Error in update_ui: {e}")  # ✅ طباعة الخطأ إذا حدث

    update_ui()  # ✅ بدء التحديث الأول

    # ✅ دالة الإغلاق مع إيقاف أي عمليات مجدولة
    def on_close():
        if "task_id" in globals():
            dashboard.after_cancel(task_id)  # ✅ إلغاء التحديث
        dashboard.destroy()  # ✅ إغلاق النافذة

    dashboard.protocol("WM_DELETE_WINDOW", on_close)  # ✅ تنفيذ on_close عند الإغلاق

    # ✅ تحديث الرصيد مع إغلاق القاعدة بعد كل استعلام
    def add_balance():
        student_id = student_id_entry.get().strip()
        try:
            amount = float(amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            return

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM students WHERE rfid = ?", (student_id,))
            result = cursor.fetchone()

            if result:
                new_balance = result[0] + amount
                cursor.execute("UPDATE students SET balance = ? WHERE rfid = ?", (new_balance, student_id))
                cursor.execute("INSERT INTO transactions (student_id, amount, admin_username) VALUES (?, ?, ?)", 
                               (student_id, amount, admin_username))
                conn.commit()
                messagebox.showinfo("Success", f"Added {amount} to student {student_id}")

                notification.notify(
                    title="Transaction Successful ✅",
                    message=f"Added {amount} to Student ID: {student_id}",
                    timeout=5
                )
            else:
                messagebox.showerror("Error", "Student not found")

    ctk.CTkButton(main_frame, text="💰 Add Balance", command=add_balance, width=250, height=50, corner_radius=10).pack(pady=10)

    dashboard.mainloop()

# ✅ دالة فتح شاشة تسجيل الدخول
def open_login_window():
    global login_window
    login_window = ctk.CTk()
    login_window.title("Admin Login")
    login_window.geometry("400x400")
    login_window.resizable(False, False)

    frame = ctk.CTkFrame(login_window, width=350, height=300, corner_radius=15)
    frame.pack(pady=20)

    ctk.CTkLabel(frame, text="🔐 Admin Login", font=("Arial", 18, "bold")).pack(pady=10)

    username_entry = ctk.CTkEntry(frame, placeholder_text="Username", width=280, height=40, corner_radius=10)
    username_entry.pack(pady=5)

    password_entry = ctk.CTkEntry(frame, placeholder_text="Password", width=220, height=40, show="*", corner_radius=10)
    password_entry.pack(pady=5)

    def login():
        username = username_entry.get()
        password = password_entry.get().encode('utf-8')

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM admins WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result:
                hashed_password = result[0]
                if isinstance(hashed_password, str):
                    hashed_password = hashed_password.encode('utf-8')

                if bcrypt.checkpw(password, hashed_password):
                    login_window.withdraw()
                    open_admin_dashboard(username)
                else:
                    messagebox.showerror("Error", "Invalid username or password")
            else:
                messagebox.showerror("Error", "Invalid username or password")

    ctk.CTkButton(frame, text="🔓 Login", command=login, width=250, height=40, corner_radius=10).pack(pady=10)
    ctk.CTkButton(frame, text="➕ Register New Admin", command=open_register_window, width=250, height=40, corner_radius=10).pack(pady=10)

    login_window.mainloop()

# ✅ دالة فتح نافذة تسجيل إداري جديد
def open_register_window():
    register_window = ctk.CTkToplevel()
    register_window.title("Register New Admin")
    register_window.geometry("350x250")
    register_window.resizable(False, False)

    frame = ctk.CTkFrame(register_window, width=300, height=200, corner_radius=15)
    frame.pack(pady=20)

    ctk.CTkLabel(frame, text="👤 Register New Admin", font=("Arial", 16, "bold")).pack(pady=10)

    new_username_entry = ctk.CTkEntry(frame, placeholder_text="New Username", width=250)
    new_username_entry.pack(pady=5)

    new_password_entry = ctk.CTkEntry(frame, placeholder_text="New Password", show="*", width=250)
    new_password_entry.pack(pady=5)

    def register_admin():
        new_username = new_username_entry.get()
        new_password = new_password_entry.get()

        if not new_username or not new_password:
            messagebox.showerror("Error", "Please enter all fields")
            return

        with get_db_connection() as conn:
            cursor = conn.cursor()
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", (new_username, hashed_password))
            conn.commit()
            messagebox.showinfo("Success", "Admin account created successfully!")
            register_window.destroy()

    ctk.CTkButton(frame, text="✅ Create Account", command=register_admin, width=250).pack(pady=10)

# ✅ البرنامج يطلب كلمة مرور قبل التشغيل
PASSWORD = "123456789"

def check_password():
    entered_password = password_entry.get()
    
    if entered_password == PASSWORD:
        password_window.destroy()
        open_login_window()
    else:
        messagebox.showerror("Error", "Incorrect password! Access denied.")
        password_window.destroy()

password_window = ctk.CTk()
password_window.title("Security Check")
password_window.geometry("300x200")
password_window.resizable(False, False)

frame = ctk.CTkFrame(password_window, width=250, height=150, corner_radius=15)
frame.pack(pady=20)

ctk.CTkLabel(frame, text="🔒 Enter Program Password:", font=("Arial", 14, "bold")).pack(pady=10)
password_entry = ctk.CTkEntry(frame, show="*", width=220)
password_entry.pack(pady=10)

ctk.CTkButton(frame, text="🔓 Unlock", command=check_password, width=220).pack(pady=5)
ctk.CTkButton(frame, text="❌ Close", command=password_window.destroy, width=220).pack(pady=5)

password_window.mainloop()