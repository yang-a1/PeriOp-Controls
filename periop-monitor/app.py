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

        self.home_screen = HomeScreen(self)
        self.monitor_mode_screen = MonitorModeScreen(self)

        self.show_screen(self.home_screen)

    def show_screen(self, screen):
        """Switch to the specified screen."""
        for widget in self.winfo_children():
            widget.pack_forget()
        screen.pack(fill="both", expand=True)

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

        self.monitor_mode_bg_img = PhotoImage(file="assets/monitor-mode/home-screen.png")
        self.home_button = tk.Button(
            self,
            image=self.monitor_mode_bg_img,
            bg="#FFFFFF",
            activebackground="#F3F6FB",
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.master.show_screen(self.master.home_screen)
        )
        self.home_button.place(x=26, y=408)

        self.help_button_img = PhotoImage(file="assets/monitor-mode/help-button.png")
        self.help_button = tk.Label(self, image=self.help_button_img, bg="#F3F6FB")
        self.help_button.place(x=750, y=22)

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

        self.monitor_mode_img = PhotoImage(file="assets/display/monitor-mode.png")
        self.monitor_mode_button = tk.Button(
            self,
            image=self.monitor_mode_img,
            bg="#FFFFFF",
            activebackground="#FFFFFF",
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.master.show_screen(self.master.monitor_mode_screen)
        )
        self.monitor_mode_button.place(x=329, y=414)

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
        self.is_on = True  # Start with OFF state

        self.button_center_x = 228.5
        self.button_center_y = 277

        self.stop_button = tk.Button(
            self,
            image=self.big_on_img,
            bg="#FFFFFF",
            activebackground="#FFFFFF",
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.update_button_position(self.big_off_img.width(), self.big_off_img.height())
        
        self.stop_button.bind("<ButtonPress-1>", self.on_press)
        self.stop_button.bind("<ButtonRelease-1>", self.on_release)

        self.mattress_temp_ex_img = PhotoImage(file="assets/settings/mattress-temp-ex.png")
        self.mattress_temp_ex = tk.Label(self, image=self.mattress_temp_ex_img, bg="#FFFFFF")
        self.mattress_temp_ex.place(x=33, y=260.43)

        self.status_panel_img = PhotoImage(file="assets/settings/status-panel.png")
        self.status_panel = tk.Label(self, image=self.status_panel_img, bg="#FFFFFF")
        self.status_panel.place(x=20, y=336)

        self.status_img = PhotoImage(file="assets/settings/status.png")
        self.status = tk.Label(self, image=self.status_img, bg="#F3F6FB")
        self.status.place(x=30, y=350)

        self.help_button_img = PhotoImage(file="assets/display/help-button.png")
        self.help_button = tk.Label(self, image=self.help_button_img, bg="#F3F6FB")
        self.help_button.place(x=757, y=23)

    def update_button_position(self, width, height):
        """Update the button position to keep its center fixed."""
        top_left_x = self.button_center_x - width // 2
        top_left_y = self.button_center_y - height // 2
        self.stop_button.place(x=top_left_x, y=top_left_y)

    def on_press(self, event):
        """Handle button press event."""
        if self.is_on:
            self.stop_button.config(image=self.small_off_img)
            self.update_button_position(self.small_off_img.width(), self.small_off_img.height())
        else:
            self.stop_button.config(image=self.small_on_img)
            self.update_button_position(self.small_on_img.width(), self.small_on_img.height())

    def on_release(self, event):
        """Handle button release event."""
        self.is_on = not self.is_on

        if self.is_on:
            self.stop_button.config(image=self.big_on_img)
            self.update_button_position(self.big_on_img.width(), self.big_on_img.height())
        else:
            self.stop_button.config(image=self.big_off_img)
            self.update_button_position(self.big_off_img.width(), self.big_off_img.height())

if __name__ == "__main__":
    app = PeriOpApp()
    app.mainloop()
