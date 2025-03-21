import os
import sqlite3
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox

# ✅ UI Settings
ctk.set_appearance_mode("dark")  # Default to dark mode
ctk.set_default_color_theme("blue")  # You can change to "green" or "dark-blue"

# ✅ Database Connection
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# ✅ Create Main Window
root = ctk.CTk()
root.title("Smart Printing System")
root.geometry("500x400")
root.resizable(False, False)  # Prevent resizing the window

# ✅ Load Background Image
image_path = "3skar.jpg"  # Make sure the image is in the same directory
try:
    image = Image.open(image_path)
    image = image.resize((500, 400))  # Adjust size
    photo = ImageTk.PhotoImage(image)

    background_label = ctk.CTkLabel(root, image=photo, text="")
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    print("⚠ Warning: Image not found!")

# ✅ Card Number Entry
card_entry = ctk.CTkEntry(root, placeholder_text="Card Number", width=250)
card_entry.place(x=120, y=30)

# ✅ Display User Name
name_label = ctk.CTkLabel(root, text="User Name: ...", font=("Arial", 14))
name_label.place(x=120, y=80)

# ✅ Display Current Balance
balance_label = ctk.CTkLabel(root, text="Available Balance: ...", font=("Arial", 14), text_color="green")
balance_label.place(x=120, y=120)

# ✅ Page Count Entry
pages_entry = ctk.CTkEntry(root, placeholder_text="Number of Pages", width=100)
pages_entry.place(x=120, y=160)

# ✅ Function to Get User Info
def get_user_info(event=None):
    card_id = card_entry.get().strip()
    if card_id:
        cursor.execute("SELECT name, balance FROM students WHERE rfid = ?", (card_id,))
        user = cursor.fetchone()
        if user:
            name, balance = user
            name_label.configure(text=f"User Name: {name}")
            balance_label.configure(text=f"Available Balance: {balance} EGP", text_color="green")
        else:
            name_label.configure(text="❌ Not Registered")
            balance_label.configure(text="❌ Not Available", text_color="red")
            messagebox.showwarning("⚠ Error", "Card number not registered!")

# ✅ Function to Print a Document
def print_document():
    file_path = r"C:\Users\LOQ\new project\test.pdf"  # Ensure this file exists
    
    if os.path.exists(file_path):
        os.startfile(file_path, "print")  # Sending the file to the default printer
        messagebox.showinfo("✅ Printing", "Document sent to the printer successfully!")
        print("📄 Document sent to printer successfully ✅")
    else:
        messagebox.showerror("⚠ Error", "File not found! Ensure the document exists.")
        print("⚠ Error: File not found!")

# ✅ Function to Deduct Printing Cost & Print
def deduct_balance():
    card_id = card_entry.get().strip()
    num_pages = pages_entry.get().strip()

    if not card_id:
        messagebox.showwarning("⚠ Error", "Please enter the card number!")
        return
    if not num_pages.isdigit() or int(num_pages) <= 0:
        messagebox.showwarning("⚠ Error", "Please enter a valid number of pages!")
        return

    num_pages = int(num_pages)
    cursor.execute("SELECT balance FROM students WHERE rfid = ?", (card_id,))
    user = cursor.fetchone()

    if user:
        balance = user[0]
        total_cost = num_pages * 1  # 1 EGP per page

        if balance >= total_cost:
            new_balance = balance - total_cost
            cursor.execute("UPDATE students SET balance = ? WHERE rfid = ?", (new_balance, card_id))
            conn.commit()
            balance_label.configure(text=f"Available Balance: {new_balance} EGP", text_color="green")

            # ✅ Print the document after successful deduction
            print_document()

            messagebox.showinfo("✅ Success", f"Printed {num_pages} pages!\nRemaining Balance: {new_balance} EGP")
            pages_entry.delete(0, ctk.END)
        else:
            balance_label.configure(text_color="red")
            messagebox.showwarning("⚠ Insufficient Balance", "Not enough balance for printing!")
    else:
        messagebox.showerror("⚠ Error", "Card number not found!")

# ✅ Search Button
search_button = ctk.CTkButton(root, text="🔍 Search", command=get_user_info, width=150)
search_button.place(x=320, y=30)

# ✅ Print & Deduct Balance Button
print_button = ctk.CTkButton(root, text="🖨 Print", command=deduct_balance, width=150)
print_button.place(x=320, y=160)

# ✅ Exit Button
exit_button = ctk.CTkButton(root, text="❌ Exit", command=root.destroy, fg_color="red", hover_color="darkred", width=150)
exit_button.place(x=180, y=270)

# ✅ Bind Enter Key to Search Function
card_entry.bind("<Return>", get_user_info)

# ✅ Run Application
root.mainloop()
