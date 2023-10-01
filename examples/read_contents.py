import sys
sys.path.append('.')
from src import USBStorage
usb_storage = USBStorage()
content = usb_storage.read("sample_poem.txt")
if content != "USB not connected":
    print("Content of example.txt:", content)
