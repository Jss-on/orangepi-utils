import sys
sys.path.append('.')
from src import USBStorage
usb_storage = USBStorage()
status = usb_storage.write("hello.txt", "Hello, World!")
if status == "USB not connected":
    print("USB is not connected. Cannot write to the file.")
