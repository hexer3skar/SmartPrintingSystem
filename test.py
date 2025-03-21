import os

def print_document():
    file_path = "C:\\Users\\3skar\\new project\\test.pdf"  # Ensure the file exists in this path
    if os.path.exists(file_path):
        os.startfile(file_path, "print")  # Send the file to the printer
        print(" File sent to the default printer ✅")
    else:
        print("⚠ File not found, check the path!")

# Example usage
print_document()