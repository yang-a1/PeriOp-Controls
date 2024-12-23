import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

class HomeScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("800x480")
        self.master.configure(bg="#E5EBF6")
        self.master.resizable(False, False)  # Prevent resizing

        # Temperature Settings Frame (LEFT)
        self.temp_settings_frame = tk.Frame(self.master, width=453, height=448, bg="#ffffff")
        self.temp_settings_frame.place(x=10, y=10)  # Position on the left

        # Mattress Temperature
        self.mattress_temp_img = PhotoImage(file="assets/mattress-temperature.png")
        self.mattress_temp_label = tk.Label(self.temp_settings_frame, image=self.mattress_temp_img, bg="#ffffff")
        self.mattress_temp_label.place(x=3, y=172)

        # Stop Button
        self.stop_button_img = PhotoImage(file="assets/STOP-buttons.png")
        self.stop_button = tk.Label(self.temp_settings_frame, image=self.stop_button_img, bg="#ffffff")
        self.stop_button.place(x=175, y=176)

        # Adjust Button
        self.adjust_button_img = PhotoImage(file="assets/adjust-button.png")
        self.adjust_button = tk.Label(self.temp_settings_frame, image=self.adjust_button_img, bg="#ffffff")
        self.adjust_button.place(x=175, y=5)

        # Temperature Display Frame (RIGHT)
        self.temp_display_frame = tk.Frame(self.master, width=469, height=452, bg="#ffffff")
        self.temp_display_frame.place(x=320, y=10)  # Position on the right

        # Temperature Display Background Image
        self.temp_display_bg = Image.open("assets/temperature-display-panel.png")
        self.temp_display_bg = ImageTk.PhotoImage(self.temp_display_bg.resize((469, 452)))
        self.temp_display_label = tk.Label(self.temp_display_frame, image=self.temp_display_bg)
        self.temp_display_label.place(x=0, y=0, width=469, height=452)

        # Language Button
        self.language_img = PhotoImage(file="assets/language.png")
        self.language_button = tk.Label(self.temp_display_frame, image=self.language_img, bg="#ffffff")
        self.language_button.place(x=357, y=413)

        # Help Button
        self.help_button_img = PhotoImage(file="assets/help-button.png")
        self.help_button = tk.Label(self.temp_display_frame, image=self.help_button_img, bg="#ffffff")
        self.help_button.place(x=436, y=9)

        # Graph Background
        self.graph_background_img = Image.open("assets/graph-background.png")
        self.graph_background_img = ImageTk.PhotoImage(self.graph_background_img.resize((400, 300)))
        self.graph_background = tk.Label(self.temp_display_frame, image=self.graph_background_img, bg="#ffffff")
        self.graph_background.place(x=50, y=40)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("PeriOp Monitor")
    app = HomeScreen(master=root)
    app.mainloop()
