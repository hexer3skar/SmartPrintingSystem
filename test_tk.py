import tkinter as tk
from PIL import Image, ImageTk
import os

# ✅ التحقق من وجود الصورة
image_path = r"C:\Users\3skar\new project\3skar.jpg"

if not os.path.exists(image_path):
    print(f"⚠ الصورة غير موجودة في: {image_path}")
else:
    print("✅ الصورة موجودة، جاري تحميلها...")

    # ✅ إنشاء نافذة Tkinter
    root = tk.Tk()
    root.title("اختبار عرض الصورة في Tkinter")
    root.geometry("600x400")

    try:
        img = Image.open(image_path)
        img = img.resize((600, 300), Image.LANCZOS)  # ✅ تعديل الحجم
        photo = ImageTk.PhotoImage(img)

        label = tk.Label(root, image=photo)
        label.image = photo  # ✅ الاحتفاظ بمرجع الصورة
        label.pack(pady=20)  # ✅ إضافة الصورة إلى الواجهة

        print("✅ الصورة تم تحميلها وعرضها بنجاح!")

        root.mainloop()
    except Exception as e:
        print(f"⚠ خطأ في تحميل الصورة: {e}")