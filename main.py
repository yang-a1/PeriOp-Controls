import Adafruit_DHT
import time

# Sensor should be set to Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT22

# GPIO pin connected to the sensor data line
pin = '17'

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        
        time.sleep(2)

except KeyboardInterrupt:
    print("\nProgram stopped by user")
