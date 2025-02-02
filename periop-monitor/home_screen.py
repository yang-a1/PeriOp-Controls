import tkinter as tk
from tkinter import PhotoImage
from utils import on_press, on_release

class HomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#E5EBF6")
        self.app = master
        self.master = master

        # Temperature Display
        self.display_panel_img = PhotoImage(file="assets/display/temperature-display-panel.png")
        self.display_panel = tk.Label(self, image=self.display_panel_img, bg="#E5EBF6")
        self.display_panel.place(x=320, y=15.62)

        self.temperature_display_img = PhotoImage(file="assets/display/temperature-display.png")
        self.temperature_display = tk.Label(self, image=self.temperature_display_img, bg="#F3F6FB")
        self.temperature_display.place(x=336.44, y=26.44)

        self.graph_background_img = PhotoImage(file="assets/display/graph-background.png")
        self.graph_background = tk.Label(self, image=self.graph_background_img, bg="#F3F6FB")
        self.graph_background.place(x=370, y=57.38)

        self.graph_lines_img = PhotoImage(file="assets/display/graph-lines.png")
        self.graph_lines = tk.Label(self, image=self.graph_lines_img, bg="#BCD4EF")
        self.graph_lines.place(x=370, y=57.38)

        self.temperatures_img = PhotoImage(file="assets/display/temperatures.png")
        self.temperatures = tk.Label(self, image=self.temperatures_img, bg="#F3F6FB")
        self.temperatures.place(x=340, y=56)

        self.is_monitor_mode_on = [True]  # State for the monitor mode button

        self.big_monitor_mode_img = PhotoImage(file="assets/display/big-monitor-mode.png")
        self.small_monitor_mode_img = PhotoImage(file="assets/display/small-monitor-mode.png")

        self.monitor_mode_button = tk.Button(
            self,
            image=self.big_monitor_mode_img,
            bg="#FFFFFF",
            activebackground="#FFFFFF",
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.master.show_screen(self.master.monitor_mode_screen)
        )

        monitor_button_center_x = 329 + self.big_monitor_mode_img.width() // 2
        monitor_button_center_y = 414 + self.big_monitor_mode_img.height() // 2

        self.monitor_mode_button.place(
            x=monitor_button_center_x - self.big_monitor_mode_img.width() // 2,
            y=monitor_button_center_y - self.big_monitor_mode_img.height() // 2
        )

        self.monitor_mode_button.bind(
            "<ButtonPress-1>",
            lambda event: self.app.on_press(
                self.monitor_mode_button,
                self.small_monitor_mode_img,
                monitor_button_center_x,
                monitor_button_center_y
            )
        )

        self.monitor_mode_button.bind(
            "<ButtonRelease-1>",
            lambda event: self.app.on_release(
                self.monitor_mode_button,
                self.is_monitor_mode_on,
                self.big_monitor_mode_img,
                self.small_monitor_mode_img,
                monitor_button_center_x,
                monitor_button_center_y
            )
        )

        self.language_img = PhotoImage(file="assets/display/language.png")
        self.language = tk.Label(self, image=self.language_img, bg="#FFFFFF")
        self.language.place(x=677, y=429)

        # Temperature Settings and Mattress Temperature 
        self.settings_panel_img = PhotoImage(file="assets/settings/temperature-settings-and-mattress-temperature-panel.png")
        self.settings_panel = tk.Label(self, image=self.settings_panel_img, bg="#E5EBF6")
        self.settings_panel.place(x=13, y=20.47)

        self.temperature_settings_img = PhotoImage(file="assets/settings/temperature-settings.png")
        self.temperature_settings = tk.Label(self, image=self.temperature_settings_img, bg="#FFFFFF")
        self.temperature_settings.place(x=20, y=32)

        self.maximum_temperature_img = PhotoImage(file="assets/settings/max-temp.png")
        self.maximum_temperature = tk.Label(self, image=self.maximum_temperature_img, bg="#FFFFFF")
        self.maximum_temperature.place(x=25, y=53)

        self.maximum_temperature_panel_img = PhotoImage(file="assets/settings/maximum-temperature-panel.png")
        self.maximum_temperature_panel = tk.Label(self, image=self.maximum_temperature_panel_img, bg="#FFFFFF")
        self.maximum_temperature_panel.place(x=17, y=66)

        self.maximum_temperature_ex_img = PhotoImage(file="assets/settings/max-temp-ex.png")
        self.maximum_temperature_ex = tk.Label(self, image=self.maximum_temperature_ex_img, bg="#FFFFFF")
        self.maximum_temperature_ex.place(x=35, y=83.56)

        self.target_temperature_img = PhotoImage(file="assets/settings/target-temp.png")
        self.target_temperature = tk.Label(self, image=self.target_temperature_img, bg="#FFFFFF")
        self.target_temperature.place(x=26, y=128)

        self.target_temperature_panel_img = PhotoImage(file="assets/settings/target-temperature-panel.png")
        self.target_temperature_panel = tk.Label(self, image=self.target_temperature_panel_img, bg="#FFFFFF")
        self.target_temperature_panel.place(x=14, y=138)

        self.target_temperature_ex_img = PhotoImage(file="assets/settings/target-temp-ex.png")
        self.target_temperature_ex = tk.Label(self, image=self.target_temperature_ex_img, bg="#FFFFFF")
        self.target_temperature_ex.place(x=35, y=155.56)

        self.adjust_1_img = PhotoImage(file="assets/settings/adjust-button.png")
        self.adjust_1 = tk.Label(self, image=self.adjust_1_img, bg="#FFFFFF")
        self.adjust_1.place(x=201, y=76)

        self.adjust_2_img = PhotoImage(file="assets/settings/adjust-button.png")
        self.adjust_2 = tk.Label(self, image=self.adjust_2_img, bg="#FFFFFF")
        self.adjust_2.place(x=201, y=143)

        self.mattress_temperature_img = PhotoImage(file="assets/settings/mattress-temperature.png")
        self.mattress_temperature = tk.Label(self, image=self.mattress_temperature_img, bg="#FFFFFF")
        self.mattress_temperature.place(x=23, y=204)

        self.big_on_img = PhotoImage(file="assets/settings/big-on.png")
        self.big_off_img = PhotoImage(file="assets/settings/big-off.png")
        self.small_on_img = PhotoImage(file="assets/settings/small-on.png")
        self.small_off_img = PhotoImage(file="assets/settings/small-off.png")

        # Initial state
        self.stop_button_center_x = 228.5
        self.stop_button_center_y = 277

        self.is_on_state = [True]  # Use a list to allow mutability in callbacks

        self.stop_button = tk.Button(
            self,
            image=self.big_on_img,
            bg="#FFFFFF",
            activebackground="#FFFFFF",
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.stop_button.place(x=self.stop_button_center_x - self.big_on_img.width() // 2, 
                            y=self.stop_button_center_y - self.big_on_img.height() // 2)

        self.stop_button.bind(
            "<ButtonPress-1>",
            lambda event: self.master.on_press( 
                self.stop_button,
                self.small_off_img,
                self.stop_button_center_x,
                self.stop_button_center_y
            )
        )

        self.stop_button.bind(
            "<ButtonRelease-1>",
            lambda event: self.master.on_release(
                self.stop_button,
                self.is_on_state,
                self.big_on_img,
                self.big_off_img,
                self.stop_button_center_x,
                self.stop_button_center_y
            )
        )

        self.mattress_temp_ex_img = PhotoImage(file="assets/settings/mattress-temp-ex.png")
        self.mattress_temp_ex = tk.Label(self, image=self.mattress_temp_ex_img, bg="#FFFFFF")
        self.mattress_temp_ex.place(x=33, y=260.43)

        self.status_panel_img = PhotoImage(file="assets/settings/status-panel.png")
        self.status_panel = tk.Label(self, image=self.status_panel_img, bg="#FFFFFF")
        self.status_panel.place(x=20, y=336)

        self.status_img = PhotoImage(file="assets/settings/status.png")
        self.status = tk.Label(self, image=self.status_img, bg="#F3F6FB")
        self.status.place(x=30, y=350)

        self.help_button_img = PhotoImage(file="assets/big-help-button.png")
        self.help_button = tk.Label(self, image=self.help_button_img, bg="#F3F6FB")
        self.help_button.place(x=757, y=23)
