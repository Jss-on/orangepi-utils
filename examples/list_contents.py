# Initialize the USBStorage class
from src import USBStorage
usb_storage = USBStorage()

# Begin the USB storage operation
if usb_storage.begin():
    print("USB is connected.")
    contents = usb_storage.ls("/")
    print("Root directory contents:", contents)
else:
    print("USB is not connected.")
