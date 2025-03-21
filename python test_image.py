from PIL import Image

image_path = r"C:\Users\3skar\new project\3skar.jpg"

try:
    img = Image.open(image_path)
    img.show()  # ✅ فتح الصورة للتأكد من أن المسار صحيح
    print("✅ الصورة تم تحميلها بنجاح!")
except Exception as e:
    print(f"⚠ خطأ في تحميل الصورة: {e}")