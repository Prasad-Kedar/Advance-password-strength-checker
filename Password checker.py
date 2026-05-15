import tkinter as tk
from tkinter import ttk
from zxcvbn import zxcvbn
import re
import random
import string

# Generate secure password
def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(16))

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

    check_password()

# Toggle password visibility
def toggle_password():
    if show_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

# Check password strength
def check_password():

    password = password_entry.get()

    result = zxcvbn(password)
    score = result['score']

    feedback = []

    # Length check
    if len(password) < 8:
        feedback.append("Password should be at least 8 characters.")

    # Uppercase check
    if not re.search(r"[A-Z]", password):
        feedback.append("Add uppercase letters.")

    # Lowercase check
    if not re.search(r"[a-z]", password):
        feedback.append("Add lowercase letters.")

    # Number check
    if not re.search(r"[0-9]", password):
        feedback.append("Add numbers.")

    # Special character check
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        feedback.append("Add special characters.")

    # Common password detection
    with open("common_passwords.txt", "r") as file:
        common_passwords = file.read().splitlines()

    if password.lower() in common_passwords:
        feedback.append("This is a very common password!")

    # Strength Levels
    levels = {
        0: ("Very Weak", "red"),
        1: ("Weak", "orange"),
        2: ("Medium", "yellow"),
        3: ("Strong", "lightgreen"),
        4: ("Very Strong", "green")
    }

    strength, color = levels[score]

    strength_label.config(
        text=f"Strength: {strength}",
        fg=color
    )

    progress['value'] = (score + 1) * 20

    # Display feedback
    if feedback:
        suggestions.config(
            text="\n".join(feedback)
        )
    else:
        suggestions.config(
            text="Excellent Password!"
        )

# Create GUI Window
root = tk.Tk()

root.title("Advanced Password Strength Checker")

root.geometry("550x500")

root.config(bg="#1e1e1e")

# Title
title = tk.Label(
    root,
    text="Password Strength Checker",
    font=("Arial", 20, "bold"),
    bg="#1e1e1e",
    fg="cyan"
)

title.pack(pady=20)

# Password Entry
password_entry = tk.Entry(
    root,
    width=35,
    font=("Arial", 14),
    show="*"
)

password_entry.pack(pady=10)

# Show Password Checkbox
show_var = tk.IntVar()

show_check = tk.Checkbutton(
    root,
    text="Show Password",
    variable=show_var,
    command=toggle_password,
    bg="#1e1e1e",
    fg="white"
)

show_check.pack()

# Check Button
check_btn = tk.Button(
    root,
    text="Check Strength",
    command=check_password,
    bg="cyan",
    font=("Arial", 12)
)

check_btn.pack(pady=10)

# Generate Button
generate_btn = tk.Button(
    root,
    text="Generate Secure Password",
    command=generate_password,
    bg="lightgreen",
    font=("Arial", 12)
)

generate_btn.pack(pady=10)

# Strength Label
strength_label = tk.Label(
    root,
    text="Strength:",
    font=("Arial", 15),
    bg="#1e1e1e",
    fg="white"
)

strength_label.pack(pady=10)

# Progress Bar
progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=300,
    mode="determinate"
)

progress.pack(pady=10)

# Suggestions
suggestions = tk.Label(
    root,
    text="",
    font=("Arial", 11),
    bg="#1e1e1e",
    fg="white",
    justify="left"
)

suggestions.pack(pady=15)

# Run Application
root.mainloop()