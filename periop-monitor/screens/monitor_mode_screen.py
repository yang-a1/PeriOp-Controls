import tkinter as tk
from tkinter import PhotoImage
from temperature_sensor_backend import get_temperature

class MonitorModeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#E5EBF6")
        self.master = master
        
        self.graph_display_panel_img = PhotoImage(file="assets/monitor-mode/graph-display-panel.png")
        self.graph_display_panel = tk.Label(self, image=self.graph_display_panel_img, bg="#E5EBF6")
        self.graph_display_panel.place(x=13.5, y=13.68)

        self.temperature_display_img = PhotoImage(file="assets/monitor-mode/temperature-display.png")
        self.temperature_display = tk.Label(self, image=self.temperature_display_img, bg="#F3F6FB")
        self.temperature_display.place(x=40, y=25)

        self.graph_background_img = PhotoImage(file="assets/monitor-mode/graph-background.png")
        self.graph_background = tk.Label(self, image=self.graph_background_img, bg="#F3F6FB")
        self.graph_background.place(x=66, y=62)

        self.graph_lines_img = PhotoImage(file="assets/monitor-mode/graph-lines.png")
        self.graph_lines = tk.Label(self, image=self.graph_lines_img, bg="#BCD4EF")
        self.graph_lines.place(x=64, y=61.3)

        self.temperatures_img = PhotoImage(file="assets/monitor-mode/temperatures.png")
        self.temperatures = tk.Label(self, image=self.temperatures_img, bg="#F3F6FB")
        self.temperatures.place(x=25.47, y=59.69)

        self.is_home_screen_on = [True]  # State for the home button

        # Home Button
        self.big_home_screen_img = PhotoImage(file="assets/monitor-mode/big-home-screen.png")
        self.small_home_screen_img = PhotoImage(file="assets/monitor-mode/small-home-screen.png")

        self.home_button = tk.Button(
            self,
            image=self.big_home_screen_img,
            bg="#F3F6FB",
            activebackground="#F3F6FB",
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.master.show_screen(self.master.home_screen)
        )

        home_button_center_x = 26 + self.big_home_screen_img.width() // 2
        home_button_center_y = 408 + self.big_home_screen_img.height() // 2

        self.home_button.place(
            x=home_button_center_x - self.big_home_screen_img.width() // 2,
            y=home_button_center_y - self.big_home_screen_img.height() // 2
        )

        self.home_button.bind(
            "<ButtonPress-1>",
            lambda event: self.master.on_press(
                self.home_button,
                self.small_home_screen_img,
                home_button_center_x,
                home_button_center_y
            )
        )

        self.home_button.bind(
            "<ButtonRelease-1>",
            lambda event: self.master.on_release(
                self.home_button,
                self.is_home_screen_on,       # Current state of home screen
                self.big_home_screen_img,     # Big screen image
                self.small_home_screen_img,   # Small screen image
                home_button_center_x,         # X-coordinate for centering
                home_button_center_y          # Y-coordinate for centering
            )
        )

        self.help_button_img = PhotoImage(file="assets/big-help-button.png")
        self.help_button = tk.Label(self, image=self.help_button_img, bg="#F3F6FB")
        self.help_button.place(x=750, y=22)
        self.help_button.bind("<ButtonPress-1>", lambda event: self.help_button.config(image=self.help_button_img_pressed))
        self.help_button.bind("<ButtonRelease-1>", lambda event: self.master.show_screen(self.master.help_manual_screen))

        self.sensor_plot = self.master.SensorPlot(self,  x=66, y=62, width=710, height=335)

        