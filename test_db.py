import sqlite3

# الاتصال بقاعدة البيانات
db = sqlite3.connect("printing_system.db.db")
cursor = db.cursor()

# جلب أسماء الجداول
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# طباعة أسماء الجداول
print("الجداول الموجودة في قاعدة البيانات:")
for table in tables:
    print(table[0])

# إغلاق الاتصال
db.close()