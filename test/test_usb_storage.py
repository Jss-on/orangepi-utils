import unittest
from unittest.mock import patch, mock_open
import sys
sys.path.append('.')
from src import USBStorage  # Modify based on your actual import path

class TestUSBStorage(unittest.TestCase):

    @patch('os.path.ismount')
    @patch('builtins.open', mock_open(read_data="data"))
    def test_read(self, mock_ismount):
        mock_ismount.return_value = True  
        storage = USBStorage()
        storage.mount_path = "/usb"
        self.assertEqual(storage.read("file.txt"), "data")
    # ... add more test cases for other methods

