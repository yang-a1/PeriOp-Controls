import time
import board
import digitalio
import busio
import adafruit_max31865

# SPI setup
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)  # Change to your CS pin

# Create sensor object
sensor = adafruit_max31865.MAX31865(
    spi,
    cs,
    rtd_nominal=1000.0,
    ref_resistor=4300.0,
    wires=4  # use 2 if needed
)

while True:
    print("Temperature:", sensor.temperature)
    print("Resistance:", sensor.resistance)
    print()
    time.sleep(2)
