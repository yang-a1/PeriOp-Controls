import RPi.GPIO as GPIO
import time

# label pin of usage to indicate yellow (info) wire
RELAY_PIN = 13 # adjust based on wiring

# initialize connnection
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

# turn on (HIGH) every two seconds
TIME_ON = 2 
# turn off (LOW) every two seconds
TIME_OFF = 2

# while loop (with two seconds condition)
while True: 
        GPIO.ouput(RELAY_PIN, GPIO.HIGH) # turn relay on
        print("ON")
        time.sleep(TIME_ON) # wait for 2 seconds
        
        GPIO.output(RELAY_PIN, GPIO.LOW)  # turn relay off
        print("OFF")
        time.sleep(TIME_OFF)  # wait for 2 seconds