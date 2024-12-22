import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("My Tkinter App")
window.geometry("400x300")

# Add a Label
label = tk.Label(window, text="Welcome to Tkinter!", font=("Arial", 14))
label.pack(pady=20)

entry = tk.Entry(window, font=("Arial", 12))
entry.pack(pady=10)

def on_button_click():
    user_input = entry.get()
    messagebox.showinfo("Info", f"You entered: {user_input}")

button = tk.Button(window, text="Submit", font=("Arial", 12), command=on_button_click)
button.pack(pady=10)

quit_button = tk.Button(window, text="Quit", font=("Arial", 12), command=window.quit)
quit_button.pack(pady=10)

window.mainloop()
