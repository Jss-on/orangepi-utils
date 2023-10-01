import unittest
from unittest.mock import patch, mock_open
from src import USBStorage  # Modify based on your actual import path

class TestUSBStorage(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="data")
    @patch("src.usb_storage.os.path.ismount")
    def test_read(self, mock_ismount, mock_file):
        mock_ismount.return_value = True
        storage = USBStorage()
        storage.mount_path = "/usb"
        self.assertEqual(storage.read("file.txt"), "data")
  
    # ... add more test cases for other methods

