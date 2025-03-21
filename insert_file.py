import sqlite3

def check_and_insert_student(rfid, name, balance):
    """Check if a student exists before inserting into the database."""
    cursor.execute("SELECT * FROM students WHERE rfid = ?", (rfid,))
    if cursor.fetchone():
        print(f"⚠ Student with RFID {rfid} already exists, insertion skipped!")
    else:
        cursor.execute("INSERT INTO students (rfid, name, balance) VALUES (?, ?, ?)", (rfid, name, balance))
        print(f"✅ New student ({name}) added successfully!")

try:
    # Connect to the database
    with sqlite3.connect("students.db") as conn:
        cursor = conn.cursor()

        # Add your information
        check_and_insert_student("2420792", "Aly Eldean Mohamed", 100.0)  # Your balance is set to 100.0

        # Insert other students
        check_and_insert_student("987654321", "Sara Mohamed", 30.5)
        check_and_insert_student("2024792", "John Doe", 50.0)

        # Commit the changes automatically
        conn.commit()

except sqlite3.IntegrityError:
    print("❌ Error: Attempted to insert a duplicate RFID!")
except sqlite3.Error as e:
    print(f"❌ Database error: {e}")

finally:
    print("🔌 Database connection closed.")
