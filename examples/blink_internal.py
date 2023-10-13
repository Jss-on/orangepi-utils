import time
import sys
sys.path.append('.')
from src import GPIO
# Assuming the GPIO class is imported or defined above this line
# Initialize the GPIO object
gpio = GPIO()

# Setup (this is optional as the pinMode is not strictly necessary for the LEDs)
gpio.pinMode("green", "out")
gpio.pinMode("red", "out")

# Loop to blink LEDs
while True:
    # Turn the green LED on
    gpio.digitalWrite("green", 1)
    # Turn the red LED off
    gpio.digitalWrite("red", 0)
    # Wait for half a second
    time.sleep(0.5)
    
    # Turn the green LED off
    gpio.digitalWrite("green", 0)
    # Turn the red LED on
    gpio.digitalWrite("red", 1)
    # Wait for half a second
    time.sleep(0.5)
