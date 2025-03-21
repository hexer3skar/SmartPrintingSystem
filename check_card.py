import sqlite3

# الاتصال بقاعدة البيانات
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# إدخال رقم الكارت
card_id = input("The number of card is: ").strip()  # إزالة أي مسافات زائدة

# البحث في قاعدة البيانات
cursor.execute("SELECT name, balance FROM students WHERE rfid = ?", (card_id,))
user = cursor.fetchone()

if user:
    name, balance = user
    print(f"✅ Card Name: {name}")
    print(f"💰 Balance: {balance} pounds")
else:
    print("⚠ This card is not in the system!")

# إغلاق الاتصال
conn.close()