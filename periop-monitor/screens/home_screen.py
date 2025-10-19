import tkinter as tk
from tkinter import PhotoImage
from temperature_sensor_backend import get_temperature
from utils.temperature_utils import load_temp_num
import json 
from pathlib import Path

try:
    from temperature_sensor_backend import get_temperature as _backend_get_temperature
except Exception:
    _backend_get_temperature = None
def read_current_temperature_text() -> str:
    """Return '36.7 C' or '--.- C' if no/invalid backend reading."""
    if _backend_get_temperature is None:
        return "--.- C"
    try:
        val = _backend_get_temperature()
        if isinstance(val, (int, float)):
            return f"{float(val):.1f} C"
        s = str(val).strip()
        if s.endswith("C") or s.endswith("°C"):
            return s.replace("°", "")
        return f"{float(s):.1f} C"
    except Exception:
        return "--.- C"
_CONFIG = Path("config.json")
_DEFAULTS = {"target_temperature_c": 37.0, "max_temperature_c": 43.0}
RESET_DEFAULTS_ON_EACH_RUN = True
def initialize_config():
    """Create or reset config.json to defaults at app start."""
    if RESET_DEFAULTS_ON_EACH_RUN or not _CONFIG.exists():
        _save_config(dict(_DEFAULTS))
def _load_config():
    if _CONFIG.exists():
        try:
            return json.loads(_CONFIG.read_text())
        except Exception:
            pass
    return dict(_DEFAULTS)
def _save_config(cfg: dict):
    _CONFIG.write_text(json.dumps(cfg, indent=2))
def get_target_temperature_c() -> float:
    return float(_load_config().get("target_temperature_c", _DEFAULTS["target_temperature_c"]))
def set_target_temperature_c(val: float):
    cfg = _load_config()
    cfg["target_temperature_c"] = float(val)
    _save_config(cfg)
def get_max_temperature_c() -> float:
    return float(_load_config().get("max_temperature_c", _DEFAULTS["max_temperature_c"]))
def set_max_temperature_c(val: float):
    cfg = _load_config()
    cfg["max_temperature_c"] = float(val)
    _save_config(cfg)
def clamp30_43(x: float) -> float:
    return max(30.0, min(43.0, float(x)))

class HomeScreen(tk.Frame):
    """
    Represents the home screen UI in the PeriOp Monitor app.

    Inherits from:
        tk.Frame: A container widget used to group related widgets together.

    Purpose:
        - Displays temperature readings and controls.
        - Includes navigation to Monitor Mode.
        - Handles state for power toggling and updates digital temperature display.
    """

    # REQUIRES: master is an instance of PeriOpApp (tk.Tk subclass)
    # MODIFIES: self
    # EFFECTS: Initializes all UI components (labels, buttons, images) on the home screen
    def __init__(self, master):
        super().__init__(master, bg="#E5EBF6")
        self.master = master

        self.is_monitor_mode_on = [True] # Mutable flag for monitor mode
        self.is_on_state = [True] # Mutable flag for stop button
        self.temp_digit_widgets = []

        self.init_temperature_panel()
        self.sensor_plot = self.master.SensorPlot(self,  x=370, y=57.38, width=400, height=335)
        self.init_monitor_mode_button()
        self.init_language_indicator()
        self.init_settings_panel()
        self.init_power_button()
        self.init_status_panel()
        self.init_help_button()

        self.update_temperature_display()
        
        self.temperature_settings = tk.Label(self, image=self.temperature_settings_img, bg="#FFFFFF")
        self.temperature_settings.place(x=20, y=32)
        self.maximum_temperature = tk.Label(self, image=self.maximum_temperature_img, bg="#FFFFFF")
        self.maximum_temperature.place(x=25, y=53)
        self.maximum_temperature_panel = tk.Label(self, image=self.maximum_temperature_panel_img, bg="#FFFFFF")
        self.maximum_temperature_panel.place(x=17, y=66)
        self.maximum_temperature_ex = tk.Label(self, image=self.maximum_temperature_ex_img, bg="#FFFFFF")
        self.maximum_temperature_ex.place(x=35, y=83.56)
        self.target_temperature = tk.Label(self, image=self.target_temperature_img, bg="#FFFFFF")
        self.target_temperature.place(x=26, y=128)
        self.target_temperature_panel = tk.Label(self, image=self.target_temperature_panel_img, bg="#FFFFFF")
        self.target_temperature_panel.place(x=14, y=138)
        self.target_temperature_ex = tk.Label(self, image=self.target_temperature_ex_img, bg="#FFFFFF")
        self.target_temperature_ex.place(x=35, y=155.56)
    
        self.max_mask = tk.Label(self, bg="#FFFFFF", borderwidth=0, highlightthickness=0)
        self.max_mask.place(x=22, y=70, width=120, height=50)

        self.target_mask = tk.Label(self, bg="#FFFFFF", borderwidth=0, highlightthickness=0)
        self.target_mask.place(x=22, y=142, width=120, height=50)

        self.max_val_var = tk.StringVar(value=f"{clamp30_43(get_max_temperature_c()):.1f}°C")
        self.max_val_lbl = tk.Label(
            self.max_mask,                
            textvariable=self.max_val_var,
            bg="#FFFFFF", fg="#0B1220",
            font=("Inter", 26, "bold"),
            borderwidth=0, highlightthickness=0
        )
        self.max_val_lbl.place(relx=0.5, rely=0.5, anchor="center")

        self.target_val_var = tk.StringVar(value=f"{clamp30_43(get_target_temperature_c()):.1f}°C")
        self.target_val_lbl = tk.Label(
            self.target_mask,             
            textvariable=self.target_val_var,
            bg="#FFFFFF", fg="#0B1220",
            font=("Inter", 26, "bold"),
            borderwidth=0, highlightthickness=0
        )
        self.target_val_lbl.place(relx=0.5, rely=0.5, anchor="center")

    def init_temperature_panel(self):
        self.display_panel_img = PhotoImage(file="assets/display/temperature-display-panel.png") # Load image
        self.display_panel = tk.Label(self, image=self.display_panel_img, bg="#E5EBF6") # Create widget
        self.display_panel.place(x=320, y=15.62) # Position

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

    # REQUIRES: Monitor mode image assets exist
    # MODIFIES: self
    # EFFECTS: Initializes monitor mode toggle button with press/release handlers
    def init_monitor_mode_button(self):
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

        center_x = 329 + self.big_monitor_mode_img.width() // 2
        center_y = 414 + self.big_monitor_mode_img.height() // 2

        self.monitor_mode_button.place(
            x=center_x - self.big_monitor_mode_img.width() // 2,
            y=center_y - self.big_monitor_mode_img.height() // 2
        )

        self.monitor_mode_button.bind(
            "<ButtonPress-1>",
            lambda event: self.master.on_press(self.monitor_mode_button, self.small_monitor_mode_img, center_x, center_y)
        )

        self.monitor_mode_button.bind(
            "<ButtonRelease-1>",
            lambda event: self.master.on_release(self.monitor_mode_button, self.is_monitor_mode_on,
                                                 self.big_monitor_mode_img, self.small_monitor_mode_img,
                                                 center_x, center_y)
        )

    # REQUIRES: Language icon image exists
    # MODIFIES: self
    # EFFECTS: Displays static language icon
    def init_language_indicator(self):
        self.language_img = PhotoImage(file="assets/display/language.png")
        self.language = tk.Label(self, image=self.language_img, bg="#FFFFFF")
        self.language.place(x=677, y=429)

    # REQUIRES: Settings panel images exist
    # MODIFIES: self
    # EFFECTS: Adds UI components for max/target temp and adjustment
    def init_settings_panel(self):
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
        self.adjust_2_img = PhotoImage(file="assets/settings/adjust-button.png")

        self.adjust_1 = tk.Button(
            self, image=self.adjust_1_img, bg="#FFFFFF", activebackground="#FFFFFF",
            borderwidth=0, highlightthickness=0, relief="flat",
            command=lambda: self.open_keypad_popup(which="max")
        )
        self.adjust_1.place(x=201, y=76)
        self.adjust_1.lift()
        self.adjust_2 = tk.Button(
            self, image=self.adjust_2_img, bg="#FFFFFF", activebackground="#FFFFFF",
            borderwidth=0, highlightthickness=0, relief="flat",
            command=lambda: self.open_keypad_popup(which="target")
        )
        self.adjust_2.place(x=201, y=143)
        self.adjust_2.lift()

        self.mattress_temperature_img = PhotoImage(file="assets/settings/mattress-temperature.png")
        self.mattress_temperature = tk.Label(self, image=self.mattress_temperature_img, bg="#FFFFFF")
        self.mattress_temperature.place(x=23, y=204)

    # REQUIRES: Power button images exist
    # MODIFIES: self
    # EFFECTS: Adds and binds stop button (on/off)
    def init_power_button(self):
        self.big_on_img = PhotoImage(file="assets/settings/big-on.png")
        self.big_off_img = PhotoImage(file="assets/settings/big-off.png")
        self.small_on_img = PhotoImage(file="assets/settings/small-on.png")
        self.small_off_img = PhotoImage(file="assets/settings/small-off.png")

        self.stop_button_center_x = 228.5
        self.stop_button_center_y = 277

        self.stop_button = tk.Button(
            self,
            image=self.big_on_img,
            bg="#FFFFFF",
            activebackground="#FFFFFF",
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.stop_button.place(
            x=self.stop_button_center_x - self.big_on_img.width() // 2,
            y=self.stop_button_center_y - self.big_on_img.height() // 2
        )

        self.stop_button.bind(
            "<ButtonPress-1>",
            lambda event: self.master.on_press(self.stop_button, self.small_off_img,
                                               self.stop_button_center_x, self.stop_button_center_y)
        )

        self.stop_button.bind(
            "<ButtonRelease-1>",
            lambda event: self.master.on_release(self.stop_button, self.is_on_state,
                                                 self.big_on_img, self.big_off_img,
                                                 self.stop_button_center_x, self.stop_button_center_y)
        )

    # REQUIRES: Status panel images exist
    # MODIFIES: self
    # EFFECTS: Adds status label to the screen
    def init_status_panel(self):
        self.status_panel_img = PhotoImage(file="assets/settings/status-panel.png")
        self.status_panel = tk.Label(self, image=self.status_panel_img, bg="#FFFFFF")
        self.status_panel.place(x=20, y=336)

        self.status_img = PhotoImage(file="assets/settings/status.png")
        self.status = tk.Label(self, image=self.status_img, bg="#F3F6FB")
        self.status.place(x=30, y=350)

    # REQUIRES: Help button image exists
    # MODIFIES: self
    # EFFECTS: Adds help button in top-right
    def init_help_button(self):
        self.help_button_img = PhotoImage(file="assets/big-help-button.png")
        self.help_button = tk.Label(self, image=self.help_button_img, bg="#F3F6FB")
        self.help_button.place(x=757, y=23)

    # REQUIRES: self has been initialized and digit images exist
    # MODIFIES: self.temp_char_list, self.temp_digit_widgets
    # EFFECTS: Periodically updates digital temperature display using digit images
    def update_temperature_display(self):
        temp_string = get_temperature()  # Example: "22.3 C"
        temp_chars = temp_string.replace(" ", "")  # "22.3C"
        if not temp_chars:
            temp_chars = ['-', '-', '.', '-', 'C']
            # TODO: Add status update (Kyle)
        digits = load_temp_num()

        if not hasattr(self, 'temp_char_list'):
            self._render_temp_chars(temp_chars, digits)

        else:
            if len(temp_chars) > len(self.temp_char_list):
                temp_chars = ['-', '-', '.', '-', 'C']
                self._render_temp_chars(temp_chars, digits)
                # TODO: Add status update (Kyle)

            else:
                for i, ch in enumerate(temp_chars):
                    if self.temp_char_list[i] != ch:
                        img = digits.get(ch)
                        self.temp_digit_widgets[i].config(image=img)
                        self.temp_digit_widgets[i].image = img
                        self.temp_char_list[i] = ch

        if self.is_on_state[0]:
            self.after(1000, self.update_temperature_display)

    # REQUIRES: digits contains mappings for all characters in temp_chars
    # MODIFIES: self.temp_char_list, self.temp_digit_widgets
    # EFFECTS: Clears and re-renders digit widgets from temp_chars
    def _render_temp_chars(self, temp_chars, digits):
        self.temp_char_list = [''] * len(temp_chars)

        for widget in getattr(self, 'temp_digit_widgets', []):
            widget.destroy()
        self.temp_digit_widgets = []

        x_cursor = 35
        y = 271.36
        spacing = 24

        for ch in temp_chars:
            img = digits.get(ch)
            label = tk.Label(self, image=img, bg="#FFFFFF")
            label.image = img
            label.place(
                x=x_cursor - 5 if ch == '.' else x_cursor + 2 if ch == 'C' else x_cursor,
                y=y + 20 if ch == '.' else y - 10 if ch == 'C' else y
            )
            self.temp_digit_widgets.append(label)

            x_cursor += (
                5 if ch == '.' else
                28 if ch == 'C' else
                spacing
            )

        self.temp_char_list = list(temp_chars)
    
    def open_keypad_popup(self, which: str):
        top = tk.Toplevel(self)
        top.title("Adjust Temperature")
        top.configure(bg="#E5EBF6")
        top.transient(self.master)
        top.grab_set()
        title = "Set Maximum (°C)" if which == "max" else "Set Target (°C)"
        tk.Label(top, text=title, bg="#E5EBF6",
                 fg="#0F172A", font=("Inter", 18, "bold")).pack(pady=(14, 6))
        buf = tk.StringVar(value="")
        entry = tk.Entry(top, textvariable=buf, font=("Inter", 28, "bold"),
                         bd=0, justify="center", readonlybackground="white")
        entry.configure(state="readonly")
        entry.pack(padx=16, pady=(0, 8), ipadx=10, ipady=8)
        def on_submit(val: str):
            try:
                v = float(val)
            except ValueError:
                tk.Label(top, text="enter a valid number", fg="#DC2626",
                         bg="#E5EBF6", font=("Inter", 12)).pack()
                return

            '''if v > 43.0:
                warn = tk.Toplevel(top)
                warn.title("Warning")
                warn.configure(bg="#FEE2E2")
                warn.transient(top)
                tk.Label(
                    warn, text="⚠️  Temperature cannot exceed 43°C",
                    bg="#FEE2E2", fg="#991B1B", font=("Inter", 14, "bold"), padx=18, pady=12
                ).pack()
                warn.after(2000, warn.destroy)
                return'''
            if v > 43.0:
                warn = tk.Toplevel(top)
                warn.title("Invalid temperature")
                warn.configure(bg="#FEE2E2")
                warn.transient(top)       # tie to the keypad window
                warn.grab_set()           # make it modal

                tk.Label(
                    warn, text="⚠️  Temperature cannot exceed 43°C",
                    bg="#FEE2E2", fg="#991B1B", font=("Inter", 14, "bold"), padx=18, pady=12
                ).pack(padx=12, pady=(12, 8))

                ok_btn = tk.Button(
                warn, text="OK", command=warn.destroy,
                bg="#3B82F6", fg="white",
                bd=0, relief="flat", highlightthickness=0,
                activebackground="#2563EB", activeforeground="white",
                font=("Inter", 13, "bold"), padx=18, pady=8, cursor="hand2"
                )
                ok_btn.pack(pady=(0, 14))
                ok_btn.update()
                warn.update_idletasks()

                warn.focus_set()
                warn.wait_window(warn)    # block until user closes it
                return

            v = clamp30_43(v)
            if which == "max":
                set_max_temperature_c(v)
                self.max_val_var.set(f"{v:.1f}°C")
            else:
                set_target_temperature_c(v)
                self.target_val_var.set(f"{v:.1f}°C")
            top.destroy()
            

        pad = NumericKeypad(top, value_var=buf, on_submit=on_submit)
        pad.pack(fill="both", expand=True, padx=16, pady=12)
    def refresh_overlays(self):
        self.max_val_var.set(f"{clamp30_43(get_max_temperature_c()):.1f}°C")
        self.target_val_var.set(f"{clamp30_43(get_target_temperature_c()):.1f}°C")

class NumericKeypad(tk.Frame):
    """On-screen keypad with big tap targets and Enter/backspace."""
    def __init__(self, master, value_var: tk.StringVar, on_submit=None, **kwargs):
        super().__init__(master, bg="#EFF3FB", **kwargs)
        self.value_var = value_var
        self.on_submit = on_submit
        self.after(0, self.lift)
        self.bind("<Map>", lambda e: self.lift())
        self.config(padx=12, pady=12)
        CELL_W, CELL_H = 120, 80
        for c in range(4):
            self.grid_columnconfigure(c, minsize=CELL_W, weight=1)
        for r in range(4):
            self.grid_rowconfigure(r, minsize=CELL_H, weight=1)
        btn_kwargs = dict(
            width=1, height=1, bd=0, relief="flat",
            font=("Inter", 24), bg="white", activebackground="#E9EEF8",
            cursor="hand2", highlightthickness=0, state="normal", takefocus=0
        )
        keys = [
            ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("0", 3, 0), (".", 3, 1),
        ]
        for text, r, c in keys:
            tk.Button(self, text=text, command=lambda t=text: self._press(t), **btn_kwargs)\
              .grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        self.back_btn = tk.Button(
            self, text="⌫", command=self._backspace,
            bg="#DADDE5", activebackground="#C9CDD6",
            fg="#1E1E1E", font=("Inter", 22), bd=0, relief="flat",
            cursor="hand2", highlightthickness=0, takefocus=0
        )
        self.back_btn.grid(row=1, column=3, padx=(10, 0), pady=10, sticky="nsew")
        self.enter_btn = tk.Button(
            self, text="→", command=self._enter,
            bg="#2E6CF6", activebackground="#2A63DE",
            fg="white", font=("Inter", 24, "bold"), bd=0, relief="flat",
            cursor="hand2", highlightthickness=0, takefocus=0
        )
        self.enter_btn.grid(row=3, column=3, padx=(10, 0), pady=10, sticky="nsew")
    def _press(self, ch: str):
        v = self.value_var.get()
        if ch == "." and "." in v:
            return
        if v == "0" and ch.isdigit():
            self.value_var.set(ch)
        else:
            self.value_var.set(v + ch)
    def _backspace(self):
        v = self.value_var.get()
        if v:
            self.value_var.set(v[:-1])
    def _enter(self):
        if self.on_submit:
            self.on_submit(self.value_var.get())

    