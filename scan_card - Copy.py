import sqlite3

def check_card(card_id):
    """التحقق من وجود الكارت وإرجاع الاسم والرصيد."""
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    print(f"🔍 DEBUG: Checking card_id={card_id} in database")  
    cursor.execute("SELECT name, balance FROM students WHERE rfid = ?", (card_id,))
    user = cursor.fetchone()

    print(f"📌 DEBUG: Query result -> {user}")  
    conn.close()
    return user

def deduct_balance(card_id, amount):
    """خصم الرصيد من الحساب إذا كان متاحًا."""
    print(f"✅ DEBUG: deduct_balance() called with card_id={card_id} and amount={amount}")  

    user = check_card(card_id)

    if user:
        name, balance = user
        print(f"✅ Card belongs to: {name}")
        print(f"💰 Current balance: {balance} pounds")

        if balance >= amount:
            new_balance = balance - amount
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE students SET balance = ? WHERE rfid = ?", (new_balance, card_id))
            conn.commit()
            conn.close()
            print(f"✅ {amount} pounds deducted! New balance: {new_balance} pounds")
        else:
            print("❌ Insufficient balance!")
    else:
        print("⚠ This card is not registered in the system!")

# ✅ تشغيل البرنامج
if __name__ == "__main__":  
    print("🔄 System is running... Please scan your card!")  
    card_id = input("🔄 Scan your card (or enter the number manually): ").strip()

    if not card_id.isdigit():
        print("⚠ Invalid card ID! Please enter numbers only.")
        exit()

    card_id = int(card_id)
    print(f"📌 Card scanned: {card_id}")  

    try:
        amount = float(input("💰 Enter the amount to deduct: "))
        if amount <= 0:
            print("❌ Invalid amount!")
        else:
            deduct_balance(card_id, amount)
    except ValueError:
        print("⚠ Please enter a valid numeric amount!")
