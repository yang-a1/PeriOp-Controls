import time
import board
import adafruit_dht
import logging

# Configure logging
logging.basicConfig(
    filename="dht_readings.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize the DHT device, with data pin connected to GPIO4
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

while True:
    try:
        # Read temperature from the DHT sensor
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32

        # Print values to the console
        print(
            "Temp: {:.1f} F / {:.1f} C".format(
                temperature_f, temperature_c
            )
        )

        # Log values to the file
        logging.info(
            "Temperature: {:.1f} F / {:.1f} C".format(
                temperature_f, temperature_c
                
            )
        )

    except RuntimeError as error:
        # Handle runtime errors and log them
        logging.warning(f"RuntimeError: {error.args[0]}")
        print(error.args[0])
        time.sleep(2.0)
        continue

    except Exception as error:
        # Log any other exceptions and raise them
        logging.error(f"Exception: {error}")
        dhtDevice.exit()
        raise error  # This is the correct way to raise the error

    # Wait before the next reading
    time.sleep(2.0)