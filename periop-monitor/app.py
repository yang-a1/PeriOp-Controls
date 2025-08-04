import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from temperature_sensor_backend import get_temperature
from screens.home_screen import HomeScreen
from screens.monitor_mode_screen import MonitorModeScreen
from utils.temperature_utils import load_temp_num

class PeriOpApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PeriOp Monitor")
        self.geometry("800x480")
        self.configure(bg="#E5EBF6")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.home_screen = HomeScreen(self)
        self.monitor_mode_screen = MonitorModeScreen(self)

        self.show_screen(self.home_screen)

    def show_screen(self, screen):
        """Switch to the specified screen."""
        for widget in self.winfo_children():
            widget.pack_forget()
        screen.pack(fill="both", expand=True)

    def on_press(self, button, small_image, button_center_x, button_center_y):
        """Handle button press event."""
        button.config(image=small_image)
        self.update_button_position(button, small_image.width(), small_image.height(), button_center_x, button_center_y)

    def on_release(self, button, is_on_state, big_on_image, big_off_image, button_center_x, button_center_y):
        """Handle button release event."""
        new_state = not is_on_state[0]  # Toggle the state
        is_on_state[0] = new_state

        if new_state:
            button.config(image=big_on_image)
            self.update_button_position(button, big_on_image.width(), big_on_image.height(), button_center_x, button_center_y)
        else:
            button.config(image=big_off_image)
            self.update_button_position(button, big_off_image.width(), big_off_image.height(), button_center_x, button_center_y)

    def update_button_position(self, button, width, height, button_center_x, button_center_y):
        """Update the button position to keep its center fixed."""
        top_left_x = button_center_x - width // 2
        top_left_y = button_center_y - height // 2
        button.place(x=top_left_x, y=top_left_y)
    
    def on_close(self):
        # Optional: add cleanup code or confirmation dialog here
        self.destroy()  # Actually closes the app