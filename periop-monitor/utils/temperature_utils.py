import tkinter as tk

def load_temp_num():
        """Load and map digit and symbol images."""
        base = "assets/temp_numbers/"
        digits = {
            '0': tk.PhotoImage(file=base + "Zero_temp.png"),
            '1': tk.PhotoImage(file=base + "One_temp.png"),
            '2': tk.PhotoImage(file=base + "Two_temp.png"),
            '3': tk.PhotoImage(file=base + "Three_temp.png"),
            '4': tk.PhotoImage(file=base + "Four_temp.png"),
            '5': tk.PhotoImage(file=base + "Five_temp.png"),
            '6': tk.PhotoImage(file=base + "Six_temp.png"),
            '7': tk.PhotoImage(file=base + "Seven_temp.png"),
            '8': tk.PhotoImage(file=base + "Eight_temp.png"),
            '9': tk.PhotoImage(file=base + "Nine_temp.png"),
            '.': tk.PhotoImage(file=base + "Dot_temp.png"),
            'C': tk.PhotoImage(file=base + "Celcius_temp.png"),
            '-': tk.PhotoImage(file=base + "Dash_temp.png"),
        }
        return digits