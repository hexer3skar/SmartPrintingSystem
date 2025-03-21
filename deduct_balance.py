import sqlite3

# الاتصال بقاعدة البيانات
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# رقم الكارت اللي عاوز تخصم منه الرصيد
rfid_card = "123456789"  # غيّره برقم كارت موجود عندك في القاعدة
amount_to_deduct = 10.0  # قيمة الخصم

# التحقق من وجود الرصيد الكافي
cursor.execute("SELECT balance FROM students WHERE rfid = ?", (rfid_card,))
result = cursor.fetchone()

if result:
    current_balance = result[0]
    if current_balance >= amount_to_deduct:
        new_balance = current_balance - amount_to_deduct
        cursor.execute("UPDATE students SET balance = ? WHERE rfid = ?", (new_balance, rfid_card))
        conn.commit()
        print(f"the success has been deducted!current balance: {new_balance}")
    else:
        print("the balance is not enough!")
else:
    print("the card not found!")

conn.close()