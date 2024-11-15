import tkinter as tk
from tkinter import messagebox
from temperature_sensor import load_config, read_temperature, control_relay
import Adafruit_DHT  # Ensure Adafruit_DHT is imported for reading sensor data

# REQUIRES: None
# MODIFIES: temperature_label (updates the displayed temperature on the UI)
# EFFECTS: Reads the temperature from the DHT22 sensor and updates the UI with the temperature value.
#          If the reading fails, an error message is displayed.
def read_sensor():
    """Reads temperature and updates the UI with the current temperature value."""
    temperature = read_temperature(Adafruit_DHT.DHT22, 17)  # GPIO pin 17 for the DHT22 sensor
    if temperature is not None:
        temperature_label.config(text=f"Temperature: {temperature:0.1f} °C")
    else:
        messagebox.showerror("Error", "Failed to read sensor data. Please try again.")
    root.after(2000, read_sensor)  # Update the sensor data every 2 seconds

# REQUIRES: temp_threshold_entry (input from the user for max temperature threshold)
#           read_temperature (function to read the temperature from the sensor)
# MODIFIES: relay_status_label (updates the UI with the relay status)
# EFFECTS: Takes the max temperature input from the user, reads the current temperature from the sensor,
#          and compares it with the threshold. If the temperature exceeds the threshold, the relay is turned off.
#          The relay status is then updated on the UI.
def control_relay_ui():
    """Controls the relay based on user input for maximum temperature."""
    try:
        max_temp = float(temp_threshold_entry.get())  # Get the max temperature from user input
        temperature = read_temperature(Adafruit_DHT.DHT22, 17)  # Read temperature from the sensor
        if temperature is not None:
            control_relay(temperature, max_temp)  # Control the relay based on temperature
            if temperature > max_temp:
                relay_status_label.config(text="Relay OFF - Temperature exceeded")  # Update relay status if exceeded
            else:
                relay_status_label.config(text="Relay ON - Temperature safe")  # Update relay status if within threshold
        else:
            messagebox.showerror("Error", "Failed to read sensor data. Please try again.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the temperature threshold.")

# REQUIRES: None
# MODIFIES: None
# EFFECTS: Sets up the main window with UI elements including temperature display, input for max temperature,
#          and relay control button. Starts the sensor reading process by calling read_sensor().
def setup_ui():
    """Sets up the user interface (UI) and starts the sensor reading loop."""
    # Set up the main window
    root = tk.Tk()
    root.title("Temperature Sensor Control")

    # Labels for temperature
    temperature_label = tk.Label(root, text="Temperature: -- °C", font=('Arial', 14))
    temperature_label.pack(pady=10)

    # Entry to set maximum temperature threshold
    temp_threshold_label = tk.Label(root, text="Enter Max Temperature (°C):", font=('Arial', 12))
    temp_threshold_label.pack(pady=5)

    temp_threshold_entry = tk.Entry(root, font=('Arial', 12))
    temp_threshold_entry.pack(pady=5)

    # Button to control relay based on temperature threshold
    control_button = tk.Button(root, text="Set Max Temp & Control Relay", font=('Arial', 12), command=control_relay_ui)
    control_button.pack(pady=10)

    # Label to show relay status
    relay_status_label = tk.Label(root, text="Relay status: --", font=('Arial', 14))
    relay_status_label.pack(pady=10)

    # Start reading sensor data
    read_sensor()

    # Run the GUI loop
    root.mainloop()

# Main entry point
if __name__ == "__main__":
    setup_ui()