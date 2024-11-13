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
    import json

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
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)  # Pin 18 is used for relay control

# REQUIRES: config (dictionary containing configuration values including "max_temperature")
# MODIFIES: relay (controls the state of the relay pin)
# EFFECTS: Reads temperature from the sensor, compares it to the max temperature threshold in config.
#          If temperature exceeds the threshold, the relay is turned off to stop the energy flow.
def main():
    """Main function that controls the temperature monitoring and relay."""
    import time
    import Adafruit_DHT

    sensor = Adafruit_DHT.DHT22
    pin = 17

    config = load_config()
    max_temperature = config.get('max_temperature', 34)  # Default to 34 if not found

    setup_gpio()

    try:
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            
            if humidity is not None and temperature is not None:
                print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))

                if temperature > max_temperature:
                    print(f"Temperature exceeds {max_temperature}°C. Turning off relay.")
                    GPIO.output(18, GPIO.LOW)  # Turn off relay
                else:
                    GPIO.output(18, GPIO.HIGH)  # Ensure relay is on if below threshold
            else:
                print('Failed to get reading. Try again!')

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nProgram stopped by user")
        GPIO.cleanup() 
