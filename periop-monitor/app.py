# Defines the main PeriOpApp class that controls screen navigation, shared UI behavior, 
# and application-level setup.

import tkinter as tk
from tkinter import PhotoImage # For displaying images in Tkinter widgets
from PIL import Image, ImageTk # Used for handling more complex image formats
from temperature_sensor_backend import get_temperature # Reads data from the DHT22 sensor
from screens.home_screen import HomeScreen
from screens.monitor_mode_screen import MonitorModeScreen
from utils.temperature_utils import load_temp_num

class PeriOpApp(tk.Tk):
    """
    Main application window for PeriOp Monitor.

    Inherits from:
        tk.Tk: The root window class from Tkinter, which provides the main
        GUI window and event loop.

    Purpose:
        - Acts as the container for all screens (home, monitor, help).
        - Handles screen switching and global state.
        - Initializes and manages the overall application UI.
    """

    # REQUIRES: None
    # MODIFIES: self
    # EFFECTS: Initializes the main app window and UI screens
    def __init__(self):
        super().__init__() #Calls constructor for tk.Tk to set up the root window
        self.title("PeriOp Monitor")
        self.geometry("800x480")
        self.configure(bg="#E5EBF6")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.destroy) # Closes window when 'X' is pressed

        self.SensorPlot = SensorPlot
        self.home_screen = HomeScreen(self)
        self.monitor_mode_screen = MonitorModeScreen(self)
        self.help_manual_screen = HelpManualScreen(self)
        for screen in (self.home_screen, self.monitor_mode_screen, self.help_manual_screen):
            screen.place(x=0, y=0, width=800, height=480)

        self.show_screen(self.home_screen)

    # REQUIRES: screen is a tk.Frame
    # MODIFIES: self
    # EFFECTS: Clears current widgets and displays the given screen
    def show_screen(self, screen):
        """Switch to the specified screen."""
        for s in (self.home_screen, self.monitor_mode_screen, self.help_manual_screen): 
            s.lower()
        screen.lift()

    # REQUIRES: button is a tk.Button, small_image is a PhotoImage
    # MODIFIES: button
    # EFFECTS: Changes button image to pressed version and repositions it
    def on_press(self, button, small_image, button_center_x, button_center_y):
        """Handle button press event."""
        button.config(image=small_image)
        self.update_button_position(button, small_image.width(), small_image.height(), button_center_x, button_center_y)

    # REQUIRES: button is a tk.Button, is_on_state is a list containing a boolean
    # MODIFIES: button, is_on_state
    # EFFECTS: Toggles button state, updates image and position
    def on_release(self, button, is_on_state, big_on_image, big_off_image, button_center_x, button_center_y):
        """Handle button release event."""
        new_state = not is_on_state[0] # Toggle the state
        is_on_state[0] = new_state

        if new_state:
            button.config(image=big_on_image)
            self.update_button_position(button, big_on_image.width(), big_on_image.height(), button_center_x, button_center_y)
        else:
            button.config(image=big_off_image)
            self.update_button_position(button, big_off_image.width(), big_off_image.height(), button_center_x, button_center_y)

    # REQUIRES: button is a tk.Button, width/height are dimensions of image
    # MODIFIES: button
    # EFFECTS: Repositions button so that its center matches given coordinates
    def update_button_position(self, button, width, height, button_center_x, button_center_y):
        """Update the button position to keep its center fixed."""
        top_left_x = button_center_x - width // 2
        top_left_y = button_center_y - height // 2
        button.place(x=top_left_x, y=top_left_y)

class SensorPlot:
    def __init__(self, parent, x=0, y=0, width=500, height=150, max_points=25):
        self.canvas = tk.Canvas(parent, width=width, height=height,
                                bg='#BCD4EF', highlightthickness=0, bd=0)
        self.canvas.place(x=x, y=y)
        self.width = width
        self.height = height
        self.max_points = max_points
        self.data = []
        self.line = None
        self.update_line()
    def update_line(self):
        try:
            new_temp = get_temperature()
            if "--" in new_temp:
                new_temp_value = self.data[-1] if self.data else 0
            else:
                new_temp_value = float(new_temp.replace(" C", "").strip())
        except:
            new_temp_value = self.data[-1] if self.data else 0
        self.data.append(new_temp_value)
        if len(self.data) > self.max_points:
            self.data.pop(0)
        max_temp = 50
        min_temp = 0
        scaled = [self.height - ((t - min_temp) / (max_temp - min_temp)) * self.height for t in self.data]
        # Clear and redraw the line
        self.canvas.delete("line")
        if len(scaled) > 1:
            coords = []
            x_spacing = self.width / (self.max_points - 1)
            for i, y in enumerate(scaled):
                coords.extend((i * x_spacing, y))
            self.canvas.create_line(*coords, fill='red', width=2, tags="line", smooth=True)
        self.canvas.after(2000, self.update_line)

class HelpManualScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#E5EBF6")
        self.master = master

        self.help_manual_img = PhotoImage(file="assets/help-manual.png")
        tk.Label(self, image=self.help_manual_img, bg="#E5EBF6").pack(padx=20, pady=20)

        self.back_button_img = PhotoImage(file="assets/exit.png")
        tk.Button(
            self,
            image=self.back_button_img,
            bg="#E5EBF6",
            activebackground="#E5EBF6",
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.master.show_screen(self.master.home_screen),
        ).place(x=700, y=35)