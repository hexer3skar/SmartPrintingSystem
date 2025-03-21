import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

class SmartPrintingApp(App):
    def build(self):
        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        # ✅ تحميل الصورة
        image = Image(source="3skar.jpg", size_hint=(1, 0.3))

        # ✅ تحديد خط مدعوم
        font_path = "ARIAL.TTF"  # تأكد من أن الخط موجود بنفس المسار

        # ✅ إدخال رقم البطاقة
        self.rfid_label = Label(text="CARD NUMBER:", font_size=18, font_name=font_path, size_hint=(1, 0.1))
        self.rfid_input = TextInput(font_size=16, multiline=False, size_hint=(1, 0.1))

        # ✅ أماكن عرض البيانات بعد البحث
        self.name_label = Label(text="USERNAME: ...", font_size=18, font_name=font_path, size_hint=(1, 0.1))
        self.balance_label = Label(text="AVAILABLE BALANCE: ...", font_size=18, font_name=font_path, size_hint=(1, 0.1))

        # ✅ عدد الصفحات الافتراضي
        self.num_pages = 1
        self.pages_label = Label(text=f"NUMBER OF PAGES: {self.num_pages}", font_size=18, font_name=font_path, size_hint=(1, 0.1))

        # ✅ زر زيادة عدد الصفحات
        add_button = Button(text="+", font_size=18, size_hint=(0.2, 0.1))
        add_button.bind(on_press=self.increase_pages)

        # ✅ زر تقليل عدد الصفحات
        subtract_button = Button(text="-", font_size=18, size_hint=(0.2, 0.1))
        subtract_button.bind(on_press=self.decrease_pages)

        # ✅ زر البحث مرتبط بدالة البحث search_user
        search_button = Button(text="🔍 SEARCH", font_size=18, size_hint=(1, 0.1))
        search_button.bind(on_press=self.search_user)

        # ✅ زر الطباعة يخصم 1 جنيه لكل صفحة
        print_button = Button(text="🖨 PRINT", font_size=18, size_hint=(1, 0.1))
        print_button.bind(on_press=self.print_document)

        # ✅ إضافة الأدوات إلى الواجهة
        self.layout.add_widget(image)
        self.layout.add_widget(self.rfid_label)
        self.layout.add_widget(self.rfid_input)
        self.layout.add_widget(self.name_label)
        self.layout.add_widget(self.balance_label)

        # ✅ إضافة التحكم في عدد الصفحات
        page_controls = BoxLayout(orientation="horizontal", spacing=10, size_hint=(1, 0.1))
        page_controls.add_widget(subtract_button)
        page_controls.add_widget(self.pages_label)
        page_controls.add_widget(add_button)

        self.layout.add_widget(page_controls)
        self.layout.add_widget(search_button)
        self.layout.add_widget(print_button)

        return self.layout

    def search_user(self, instance):
        rfid = self.rfid_input.text.strip()

        if not rfid:
            self.name_label.text = "USERNAME: Please enter a card number"
            self.balance_label.text = "AVAILABLE BALANCE: --"
            return

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT name, balance FROM students WHERE rfid = ?", (rfid,))
            user = cursor.fetchone()

            if user:
                self.name_label.text = f"USERNAME: {user[0]}"
                self.balance_label.text = f"AVAILABLE BALANCE: {user[1]}"
            else:
                self.name_label.text = "USERNAME: Not Found"
                self.balance_label.text = "AVAILABLE BALANCE: --"

        except sqlite3.Error as e:
            self.name_label.text = "DATABASE ERROR"
            self.balance_label.text = f"Error: {e}"
        finally:
            conn.close()

    def increase_pages(self, instance):
        self.num_pages += 1
        self.pages_label.text = f"NUMBER OF PAGES: {self.num_pages}"
        print(f"✅ Pages Increased: {self.num_pages}")  # Debug

    def decrease_pages(self, instance):
        if self.num_pages > 1:
            self.num_pages -= 1
            self.pages_label.text = f"NUMBER OF PAGES: {self.num_pages}"
            print(f"✅ Pages Decreased: {self.num_pages}")  # Debug
        else:
            print("❌ Cannot decrease below 1")

    def print_document(self, instance):
        rfid = self.rfid_input.text.strip()
        pages_to_print = self.num_pages
        cost_per_page = 1
        total_cost = pages_to_print * cost_per_page

        if not rfid:
            self.balance_label.text = "AVAILABLE BALANCE: Please enter a card number"
            return

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT balance FROM students WHERE rfid = ?", (rfid,))
            result = cursor.fetchone()

            if result:
                current_balance = result[0]

                if current_balance >= total_cost:
                    new_balance = current_balance - total_cost
                    cursor.execute("UPDATE students SET balance = ? WHERE rfid = ?", (new_balance, rfid))
                    conn.commit()

                    # ✅ تحديث الواجهة بعد الخصم
                    self.balance_label.text = f"AVAILABLE BALANCE: {new_balance}"
                    self.pages_label.text = "NUMBER OF PAGES: 1"
                    self.num_pages = 1

                    print("✅ Printing successful. Balance updated.")
                else:
                    self.balance_label.text = "AVAILABLE BALANCE: Insufficient funds"
                    print("❌ Not enough balance to print.")
            else:
                self.balance_label.text = "AVAILABLE BALANCE: User Not Found"
                print("❌ User not found in database.")

        except sqlite3.Error as e:
            self.balance_label.text = "DATABASE ERROR"
            print(f"❌ Database error: {e}")

        finally:
            conn.close()

if __name__ == "__main__":
    SmartPrintingApp().run()
