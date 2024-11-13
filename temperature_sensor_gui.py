import Adafruit_DHT
import time
import json
import RPi.GPIO as GPIO

# REQUIRES: None
# MODIFIES: config (dictionary storing configuration values)
# EFFECTS: Reads a JSON configuration file and loads the configuration values into a dictionary.
#          Assumes the config file is in JSON format and contains a "max_temperature" key.
def load_config():
    """Loads configuration settings from a config file."""
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        return config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading config: {e}")
        return {}

# REQUIRES: GPIO library should be available and correctly configured for use with Raspberry Pi.
# MODIFIES: GPIO setup (sets the mode and relay pin for controlling the transistor)
# EFFECTS: Configures the GPIO pin 18 for output and sets the initial state for controlling the relay.
#          Disables GPIO warnings and uses BCM pin-numbering scheme.
def setup_gpio():
    """Sets up the GPIO pin for controlling the relay."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)  # Pin 18 is used for relay control

# REQUIRES: config (dictionary containing configuration values including "max_temperature")
# MODIFIES: GPIO relay state (turns relay on or off)
# EFFECTS: Compares current temperature with configured threshold, and controls relay accordingly.
def control_relay(temperature, max_temperature):
    """Controls the relay based on the temperature compared to max_temperature."""
    if temperature > max_temperature:
        print(f"Temperature exceeds {max_temperature}°C. Turning off relay.")
        GPIO.output(18, GPIO.LOW)  # Turn off relay
    else:
        GPIO.output(18, GPIO.HIGH)  # Ensure relay is on if below threshold

# REQUIRES: None
# MODIFIES: None
# EFFECTS: Reads temperature from the DHT22 sensor, logs it, and controls the relay if necessary.
def read_temperature(sensor, pin):
    """Reads temperature and humidity from the sensor and returns the temperature."""
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print(f'Temperature: {temperature:0.1f}°C  Humidity: {humidity:0.1f}%')
        return temperature
    else:
        print('Failed to get reading. Try again!')
        return None

# REQUIRES: config (loaded configuration dictionary)
# MODIFIES: GPIO state
# EFFECTS: Continuously reads temperature from sensor and controls relay.
def main():
    """Main function that controls the temperature monitoring and relay."""
    sensor = Adafruit_DHT.DHT22
    pin = 17  # GPIO pin where sensor is connected

    config = load_config()
    max_temperature = config.get('max_temperature', 34)  # Default max temperature if not found

    setup_gpio()

    try:
        while True:
            temperature = read_temperature(sensor, pin)
            if temperature is not None:
                control_relay(temperature, max_temperature)
            time.sleep(2)  # Delay between readings

    except KeyboardInterrupt:
        print("\nProgram stopped by user")
        GPIO.cleanup()  # Clean up GPIO settings when exiting
