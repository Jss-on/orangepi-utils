import sys
sys.path.append('.')
import time
from src import Audio, GPIO, USBStorage

#setup GPIO for lED indicators and push buttons

gpio = GPIO()

#Starting to run -> blinking PA20
def led_indicator(time_interval=1, max_blink = 3):
    gpio.pinMode("PA20", "out")
    # Blink the LED
    count_blink = 0
    while True:
        # Turn the LED on
        gpio.digitalWrite("PA20", 1)
        time.sleep(time_interval)  # Wait for 1 second

        # Turn the LED off
        gpio.digitalWrite("PA20", 0)
        time.sleep(time_interval)  # Wait for 1 second

        if count_blink == max_blink:
            count_blink = 0
            break
        
        count_blink += 1


def push_button_indicator():
    # Configure PA10 as an input pin
    gpio.pinMode("PG8", "in")
    gpio.pinMode("PA10", "out")
    # Monitor the button
    count = 0
    while True:
        # Read the state of the button
        button_state = gpio.digitalRead("PG8")

        if count != 0:
            # Turn the LED on
            gpio.digitalWrite("PA10", 1)
        
        if button_state == 1:
            count = 0
            print("Button is pressed.")
        else:
            count += 1
            print("Button is not pressed.")
        
        if count == 15:
            led_indicator(time_interval=0.2, max_blink=15)
            gpio.digitalWrite("PA10", 0)
            break

        time.sleep(0.2)  # Poll every 200 milliseconds






#setup for USB storage


#setup for audio record

if __name__ == "__main__":
    led_indicator()
    push_button_indicator()