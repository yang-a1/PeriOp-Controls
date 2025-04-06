import time
import board
import adafruit_dht

try:
    dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
except Exception as e:
    print(f"[ERROR] Failed to initialize DHT22: {e}")
    dhtDevice = None

def get_temperature():
    if not dhtDevice:
        return "--.- C"

    try:
        temperature_c = dhtDevice.temperature
        if temperature_c is not None:
            return f"{temperature_c:.1f} C"
        else:
            return "--.- C"
    except RuntimeError:
        return "--.- C"
    except Exception as e:
        return f"Error: {e}"