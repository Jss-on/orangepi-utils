from src import USBStorage
usb_storage = USBStorage()
content = usb_storage.read("example.txt")
if content != "USB not connected":
    print("Content of example.txt:", content)
