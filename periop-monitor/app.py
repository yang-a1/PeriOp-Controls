import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

class PeriOpApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PeriOp Monitor")
        self.geometry("800x480")
        self.configure(bg="#E5EBF6")
        self.resizable(False, False)

        # Screens
        self.home_screen = HomeScreen(self)
        self.monitor_mode_screen = MonitorModeScreen(self)
        self.help_manual_screen = HelpManualScreen(self) # New change


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

    # Beginning of New Code    
class HelpManualScreen(tk.Frame): 
    def __init__(self, master):
        super().__init__(master, bg="#E5EBF6")
        self.master = master

        self.help_manual_img = PhotoImage(file="assets/help-manual.png")
        self.help_manual_label = tk.Label(self, image=self.help_manual_img, bg="#E5EBF6")
        self.help_manual_label.pack(padx=20, pady=20)

        self.back_button_img = PhotoImage(file="assets/exit.png")  
        self.back_button_label = tk.Label(self, image=self.help_manual_img, bg="#E5EBF6")
        self.back_button_label.pack(padx=20, pady=20)

        self.back_button = tk.Button(
            self, image=self.back_button_img,bg="#E5EBF6",activebackground="#E5EBF6",borderwidth=0,highlightthickness=0,relief="flat",
            command=lambda: self.master.show_screen(self.master.home_screen)
        )

        # To place the button at the top-right corner, we use x and y coordinates
        self.back_button.place(x=700, y=35)

        # End of new code

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

        # New code: command to switch to Help Manual Screen
        self.help_button.bind("<ButtonPress-1>", lambda event: self.help_button.config(image=self.help_button_img_pressed))
        self.help_button.bind("<ButtonRelease-1>", lambda event: self.master.show_screen(self.master.help_manual_screen))

class HomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#E5EBF6")
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
            lambda event: self.master.on_press(  # Use self.master.on_press
                self.monitor_mode_button,
                self.small_monitor_mode_img,
                monitor_button_center_x,
                monitor_button_center_y
            )
        )

        self.monitor_mode_button.bind(
            "<ButtonRelease-1>",
            lambda event: self.master.on_release(  # Use self.master.on_release
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
            lambda event: self.master.on_press(  # Use self.master.on_press
                self.stop_button,
                self.small_off_img,
                self.stop_button_center_x,
                self.stop_button_center_y
            )
        )

        self.stop_button.bind(
            "<ButtonRelease-1>",
            lambda event: self.master.on_release(  # Use self.master.on_release
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

        # New code: command to switch to Help Manual Screen
        self.help_button.bind("<ButtonPress-1>", lambda event: self.help_button.config(image=self.help_button_img_pressed))
        self.help_button.bind("<ButtonRelease-1>", lambda event: self.master.show_screen(self.master.help_manual_screen))
if __name__ == "__main__":
    app = PeriOpApp()
    app.mainloop()
