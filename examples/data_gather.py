import sys
sys.path.append('.')
import os
import time
import datetime
from src import Audio, GPIO, USBStorage

#setup GPIO for lED indicators and push buttons

gpio = GPIO()

#Starting to run -> blinking PA20
def led_indicator(pin="PA20", time_interval=1, max_blink = 3):
    gpio.pinMode(pin, "out")
    # Blink the LED
    count_blink = 0
    while True:
        # Turn the LED on
        gpio.digitalWrite(pin, 1)
        time.sleep(time_interval)  # Wait for 1 second

        # Turn the LED off
        gpio.digitalWrite(pin, 0)
        time.sleep(time_interval)  # Wait for 1 second

        if count_blink == max_blink:
            count_blink = 0
            break
        
        count_blink += 1


def push_button_indicator():
    # Configure PA10 as an input pin
    gpio.pinMode("PG8", "in")
    gpio.pinMode("PA10", "out")
    gpio.pinMode("PA20", "out")
    # Monitor the button
    count = 0
    while True:
        # Read the state of the button
        button_state = gpio.digitalRead("PG8")

        if count != 0:
            # Turn the LED on
            gpio.digitalWrite("PA10", 1)
        else:
            gpio.digitalWrite("PA10", 0)
        
        if button_state == 1:
            count = 0
            print("Button is pressed.")
        else:
            count += 1
            print("Button is not pressed.")
        print(f"Count: {count}")
        if count == 15:
            led_indicator(time_interval=0.2, max_blink=15)
            led_indicator(pin="PA10",time_interval=0.2, max_blink=15)
            gpio.digitalWrite("PA10", 0)
            break

        time.sleep(0.2)  # Poll every 200 milliseconds




#setup for USB storage
def main():
    usb_storage = USBStorage()
    #setup for audio record
    audio = Audio()

    mount_path = usb_storage.get_mount_path()
    led_indicator()
    push_button_indicator()
    
    
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"recording_{timestamp}.wav"
    file_path = os.path.join(f"{mount_path}",f"{file_name}")



    #setup for audio record
    audio = Audio()
    # Set custom settings
    audio.setFilename(file_path)
    audio.setDuration(30)  # 10 seconds
    audio.setRate(16000)   # 22.05 kHz
    # Record audio
    audio.recordAudio()

if __name__ == "__main__":
    main()