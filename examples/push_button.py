# Initialize the GPIO class
import time
import sys
sys.path.append('.')
from src import GPIO
gpio = GPIO()

# Configure PA10 as an input pin
gpio.pinMode("PA10", "in")

# Monitor the button
while True:
    # Read the state of the button
    button_state = gpio.digitalRead("PA10")
    
    if button_state == 1:
        print("Button is pressed.")
    else:
        print("Button is not pressed.")
        
    time.sleep(0.2)  # Poll every 200 milliseconds
