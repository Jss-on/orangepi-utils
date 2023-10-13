import time
import sys
sys.path.append('.')
import uuid

unique_id = str(uuid.uuid4())
import os
import datetime
from src import Audio, GPIO, USBStorage
# Assuming the GPIO class is imported or defined above this line
# Initialize the GPIO object
gpio = GPIO()

# Setup (this is optional as the pinMode is not strictly necessary for the LEDs)
gpio.pinMode("green", "out")
gpio.pinMode("red", "out")

count = 0
# Loop to blink LEDs
while True:
    if count == 10:
        #solid led
        gpio.digitalWrite("green", 0)
        gpio.digitalWrite("red", 0)
        time.sleep(2)
        break
    else:
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
        count += 1


usb_storage = USBStorage()
#setup for audio record


mount_path = usb_storage.get_mount_path()

unique_id = str(uuid.uuid4())

folder_name = f"data_{unique_id}"
usb_storage.append('records.txt',folder_name)
usb_storage.mkdir(folder_name)

data_counter = 0
while True:
    try:
        
        gpio.digitalWrite("green", 1)
        file_name = f"recording_{data_counter}.wav"
        file_path = os.path.join(f"{mount_path}",folder_name,f"{file_name}")

        data_counter += 1

        #setup for audio record
        audio = Audio()
        # Set custom settings
        audio.setFilename(file_path)
        audio.setDuration(10)  # 10 seconds
        audio.setRate(16000)   # 22.05 kHz
        # Record audio
        gpio.digitalWrite("red", 1)
        audio.recordAudio()
        for i in range(10):
            gpio.digitalWrite("green", 0)
            gpio.digitalWrite("red", 0)
            time.sleep(0.1)
            gpio.digitalWrite("green", 1)
            gpio.digitalWrite("red", 1)
    except KeyboardInterrupt:
        print("Done")
        break