import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

class PasswordGenerator:
    def __init__(self, window):
        self.window = window
        self.window.title("Random Password Generator")
        self.window.geometry("500x500")
        self.history_file = "history.json"

        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        tk.Label(self.window, text="Длина пароля:").pack(pady=(10, 0))
        self.length_var = tk.IntVar(value=12)
        self.slider = tk.Scale(self.window, from_=4, to=32, orient="horizontal", variable=self.length_var)
        self.slider.pack(fill="x", padx=20)

        self.use_digits = tk.BooleanVar(value=True)
        tk.Checkbutton(self.window, text="Цифры (0-9)", variable=self.use_digits).pack(anchor="w", padx=20)

        self.use_letters = tk.BooleanVar(value=True)
        tk.Checkbutton(self.window, text="Буквы (a-z, A-Z)", variable=self.use_letters).pack(anchor="w", padx=20)

        self.use_special = tk.BooleanVar(value=False)
        tk.Checkbutton(self.window, text="Спецсимволы (!@#$%^&*)", variable=self.use_special).pack(anchor="w", padx=20)

        self.password_entry = tk.Entry(self.window, font=("Arial", 14), justify="center")
        self.password_entry.pack(pady=10, fill="x", padx=20)

        tk.Button(self.window, text="Сгенерировать", command=self.generate_password, bg="#4CAF50", fg="white").pack(pady=10)

        tk.Label(self.window, text="История:").pack()
        self.tree = ttk.Treeview(self.window, columns=("Password"), show="headings", height=8)
        self.tree.heading("Password", text="Пароль")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def generate_password(self):
        length = self.length_var.get()
        
        chars = ""
        if self.use_digits.get(): chars += string.digits
        if self.use_letters.get(): chars += string.ascii_letters
        if self.use_special.get(): chars += string.punctuation

        if not chars:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
            return

        password = "".join(random.choice(chars) for _ in range(length))
        
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        
        self.save_to_history(password)

    def save_to_history(self, password):
        self.tree.insert("", 0, values=(password,))
        
        history = []
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                history = json.load(f)
        
        history.append(password)
        with open(self.history_file, "w") as f:
            json.dump(history[-20:], f)

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                history = json.load(f)
                for pwd in reversed(history):
                    self.tree.insert("", "end", values=(pwd,))

if __name__ == "__main__":
    window = tk.Tk()
    app = PasswordGenerator(window)
    window.mainloop()