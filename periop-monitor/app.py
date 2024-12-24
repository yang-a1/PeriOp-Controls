import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

class HomeScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("800x480")
        self.master.configure(bg="#E5EBF6")
        self.master.resizable(False, False)

        # Temperature Display
        self.display_panel_img = PhotoImage(file="assets/display/temperature-display-panel.png")
        self.display_panel = tk.Label(self.master, image=self.display_panel_img, bg="#E5EBF6")
        self.display_panel.place(x=320, y=15.62)

        self.temperature_display_img = PhotoImage(file="assets/display/temperature-display.png")
        self.temperature_display = tk.Label(self.master, image=self.temperature_display_img, bg="#F3F6FB")
        self.temperature_display.place(x=336.44, y=26.44)

        self.graph_background_img = PhotoImage(file="assets/display/graph-background.png")
        self.graph_background = tk.Label(self.master, image=self.graph_background_img, bg="#F3F6FB")
        self.graph_background.place(x=370, y=57.38)

        self.graph_lines_img = PhotoImage(file="assets/display/graph-lines.png")
        self.graph_lines = tk.Label(self.master, image=self.graph_lines_img, bg="#BCD4EF")
        self.graph_lines.place(x=370, y=57.38)
        
        self.temperatures_img = PhotoImage(file="assets/display/temperatures.png")
        self.temperatures = tk.Label(self.master, image=self.temperatures_img, bg="#F3F6FB")
        self.temperatures.place(x=340, y=56)

        self.monitor_mode_img = PhotoImage(file="assets/display/monitor-mode.png")
        self.monitor_mode = tk.Label(self.master, image=self.monitor_mode_img, bg="#FFFFFF")
        self.monitor_mode.place(x=329, y=414)

        self.language_img = PhotoImage(file="assets/display/language.png")
        self.language = tk.Label(self.master, image=self.language_img, bg="#FFFFFF")
        self.language.place(x=677, y=429)

        # Temperature Settings and Mattress Temperature 
        self.settings_panel_img = PhotoImage(file="assets/settings/temperature-settings-and-mattress-temperature-panel.png")
        self.settings_panel = tk.Label(self.master, image=self.settings_panel_img, bg="#E5EBF6")
        self.settings_panel.place(x=13, y=20.47)

        self.temperature_settings_img = PhotoImage(file="assets/settings/temperature-settings.png")
        self.temperature_settings = tk.Label(self.master, image=self.temperature_settings_img, bg="#FFFFFF")
        self.temperature_settings.place(x=20, y=32)

        self.maximum_temperature_img = PhotoImage(file="assets/settings/max-temp.png")
        self.maximum_temperature = tk.Label(self.master, image=self.maximum_temperature_img, bg="#FFFFFF")
        self.maximum_temperature.place(x=25, y=53)

        self.maximum_temperature_panel_img = PhotoImage(file="assets/settings/maximum-temperature-panel.png")
        self.maximum_temperature_panel = tk.Label(self.master, image=self.maximum_temperature_panel_img, bg="#FFFFFF")
        self.maximum_temperature_panel.place(x=17, y=66)

        self.maximum_temperature_ex_img = PhotoImage(file="assets/settings/max-temp-ex.png")
        self.maximum_temperature_ex = tk.Label(self.master, image=self.maximum_temperature_ex_img, bg="#FFFFFF")
        self.maximum_temperature_ex.place(x=35, y=83.56)

        self.target_temperature_img = PhotoImage(file="assets/settings/target-temp.png")
        self.target_temperature = tk.Label(self.master, image=self.target_temperature_img, bg="#FFFFFF")
        self.target_temperature.place(x=26, y=128)

        self.target_temperature_panel_img = PhotoImage(file="assets/settings/target-temperature-panel.png")
        self.target_temperature_panel = tk.Label(self.master, image=self.target_temperature_panel_img, bg="#FFFFFF")
        self.target_temperature_panel.place(x=14, y=138)

        self.target_temperature_ex_img = PhotoImage(file="assets/settings/target-temp-ex.png")
        self.target_temperature_ex = tk.Label(self.master, image=self.target_temperature_ex_img, bg="#FFFFFF")
        self.target_temperature_ex.place(x=35, y=155.56)

        self.adjust_1_img = PhotoImage(file="assets/settings/adjust-button.png")
        self.adjust_1 = tk.Label(self.master, image=self.adjust_1_img, bg="#FFFFFF")
        self.adjust_1.place(x=201, y=76)

        self.adjust_2_img = PhotoImage(file="assets/settings/adjust-button.png")
        self.adjust_2 = tk.Label(self.master, image=self.adjust_2_img, bg="#FFFFFF")
        self.adjust_2.place(x=201, y=143)

        self.mattress_temperature_img = PhotoImage(file="assets/settings/mattress-temperature.png")
        self.mattress_temperature = tk.Label(self.master, image=self.mattress_temperature_img, bg="#FFFFFF")
        self.mattress_temperature.place(x=23, y=204)

        self.on_img = PhotoImage(file="assets/settings/on.png")
        self.off_img = PhotoImage(file="assets/settings/off.png")
        
        self.is_on = False 
        self.stop_button = tk.Button(
            self.master, 
            image=self.off_img, 
            bg="#FFFFFF", 
            activebackground="#FFFFFF",  # Ensure consistency on press
            borderwidth=0, 
            highlightthickness=0, 
            relief="flat", 
            command=self.toggle_state
        )
        self.stop_button.place(x=154, y=229)

        self.mattress_temp_ex_img = PhotoImage(file="assets/settings/mattress-temp-ex.png")
        self.mattress_temp_ex = tk.Label(self.master, image=self.mattress_temp_ex_img, bg="#FFFFFF")
        self.mattress_temp_ex.place(x=33, y=260.43)

        self.status_panel_img = PhotoImage(file="assets/settings/status-panel.png")
        self.status_panel = tk.Label(self.master, image=self.status_panel_img, bg="#FFFFFF")
        self.status_panel.place(x=20, y=336)

        self.status_img = PhotoImage(file="assets/settings/status.png")
        self.status = tk.Label(self.master, image=self.status_img, bg="#F3F6FB")
        self.status.place(x=30, y=350)

    def toggle_state(self):
        """Toggle between ON and OFF state."""
        # Simulate animation by slightly changing the button's size
        self.stop_button.place(x=156, y=231)  # Slightly shrink
        self.stop_button.after(100, lambda: self.stop_button.place(x=154, y=229))  # Reset to normal

        # Toggle the state
        if self.is_on:
            self.stop_button.config(image=self.off_img)
        else:
            self.stop_button.config(image=self.on_img)

        # Change the state
        self.is_on = not self.is_on

    def expand_button(self):
        """Expand the button back to normal size."""
        self.stop_button.config(relief="raised")

        
if __name__ == "__main__":
    root = tk.Tk()
    root.title("PeriOp Monitor")
    app = HomeScreen(master=root)
    app.mainloop()
