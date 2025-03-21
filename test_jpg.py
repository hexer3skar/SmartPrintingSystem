import tkinter as tk
from PIL import Image, ImageTk
import os

# ✅ إنشاء نافذة جديدة
root = tk.Tk()
root.title("اختبار عرض الصورة داخل نافذة Tkinter")
root.geometry("600x500")

# ✅ التحقق من أن الصورة موجودة
image_path = r"C:\Users\3skar\new project\3skar.jpg"

if os.path.exists(image_path):
    try:
        img = Image.open(image_path)
        img = img.resize((600, 300), Image.LANCZOS)  # ✅ ضبط الحجم
        photo = ImageTk.PhotoImage(img)

        label = tk.Label(root, image=photo)
        label.image = photo  # ✅ الاحتفاظ بمرجع الصورة
        label.pack(pady=20)  # ✅ إضافة الصورة إلى الواجهة

        print("✅ الصورة تم تحميلها وعرضها بنجاح!")

    except Exception as e:
        print(f"⚠ خطأ في تحميل الصورة: {e}")
else:
    print(f"⚠ لم يتم العثور على الصورة في: {image_path}")

root.mainloop()