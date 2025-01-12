import tkinter as tk
from tkinter import messagebox, font
import subprocess
import sys

def take_attendance():
    try:
        subprocess.Popen([sys.executable, "Attendance_taker.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start Attendance Taker: {e}")

def update_database():
    try:
        subprocess.Popen([sys.executable, "Face_encoder.py"])
        messagebox.showinfo("Success", "Database updated successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update database: {e}")

class AttendanceSystem(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Attendance System")
        self.iconbitmap("Resources/icon.ico")
        self.geometry("400x300")
        self.configure(bg="#f0f0f0")

        self.create_widgets()

    def create_widgets(self):
        title_font = font.Font(family="Helvetica", size=18, weight="bold")
        button_font = font.Font(family="Helvetica", size=12)

        title_label = tk.Label(self, text="Attendance System", font=title_font, bg="#f0f0f0", fg="#333333")
        title_label.pack(pady=20)

        take_attendance_button = tk.Button(
            self, text="Take Attendance", command=take_attendance,
            font=button_font, bg="#4CAF50", fg="white", activebackground="#45a049",
            width=20, height=2, relief=tk.RAISED, bd=0
        )
        take_attendance_button.pack(pady=10)

        update_database_button = tk.Button(
            self, text="Update Database", command=update_database,
            font=button_font, bg="#008CBA", fg="white", activebackground="#007B9A",
            width=20, height=2, relief=tk.RAISED, bd=0
        )
        update_database_button.pack(pady=10)

        # Add hover effect
        for button in (take_attendance_button, update_database_button):
            button.bind("<Enter>", lambda e, b=button: b.config(bg=b.cget("activebackground")))
            button.bind("<Leave>", lambda e, b=button: b.config(bg=b.cget("bg")))

def main():
    app = AttendanceSystem()
    app.mainloop()

if __name__ == "__main__":
    main()