import sqlite3

def check_rfid(rfid):
    """Check if an RFID exists in the students database."""
    try:
        # Connect to the database
        with sqlite3.connect("students.db") as conn:
            cursor = conn.cursor()

            # Check if RFID exists
            cursor.execute("SELECT * FROM students WHERE rfid = ?", (rfid,))
            existing_data = cursor.fetchone()

            if existing_data:
                print(f"✔ RFID {rfid} exists in the database: {existing_data}")
            else:
                print(f"❌ RFID {rfid} not found. Please add it first.")

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")

# Change this to any RFID you want to check
rfid_to_check = "2420792"
check_rfid(rfid_to_check)
