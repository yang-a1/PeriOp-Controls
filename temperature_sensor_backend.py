import time
import board
import adafruit_dht

# Initialize the DHT device
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

def get_temperature():
    try:
        # Read temperature from the DHT sensor
        temperature_c = dhtDevice.temperature
        if temperature_c is not None:
            temperature_f = temperature_c * (9 / 5) + 32
            return f"{temperature_f:.1f} F / {temperature_c:.1f} C"
        else:
            return "-- C"  # Return a placeholder if sensor data is unavailable
    except RuntimeError as error:
        # If there's a runtime error, log it and return a placeholder message
        return "-- C"
