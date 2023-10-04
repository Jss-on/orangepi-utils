import sys

sys.path.append(".")
from src import USBStorage

usb_storage = USBStorage()
status = usb_storage.write("inference_result.txt", "Inference Results")
if status == "USB not connected":
    print("USB is not connected. Cannot write to the file.")
