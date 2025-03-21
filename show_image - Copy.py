import tkinter as tk
from PIL import Image, ImageTk  # مكتبة لمعالجة الصور

# إنشاء نافذة التطبيق
root = tk.Tk()
root.title("Smart Printing System")  # عنوان النافذة
root.geometry("600x400")  # حجم النافذة

# تحميل الصورة
image_path = "3skar.jpg"  # تأكد من الاسم الصحيح للصورة
image = Image.open(image_path)
image = image.resize((300, 200))  # تغيير الحجم (اختياري)
photo = ImageTk.PhotoImage(image)

# عرض الصورة في الواجهة
label = tk.Label(root, image=photo)
label.pack(pady=20)  # إضافة مسافة تحت الصورة

# تشغيل الواجهة
root.mainloop()