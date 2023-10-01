#!/usr/bin/bash
python3 -m unittest test/test_gpio.py
python3 -m unittest test/test_audio.py
python3 -m unittest test/test_usb_storage.py