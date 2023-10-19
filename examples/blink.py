import time
import sys

sys.path.append(".")
from src import GPIO

# Initialize the GPIO class
gpio = GPIO()

# Configure PA20 as an output pin
gpio.pinMode("PA20", "out")

# Blink the LED
while True:
    # Turn the LED on
    gpio.digitalWrite("PA20", 1)
    time.sleep(1)  # Wait for 1 second

    # Turn the LED off
    gpio.digitalWrite("PA20", 0)
    time.sleep(1)  # Wait for 1 second
