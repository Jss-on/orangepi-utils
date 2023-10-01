import unittest
from unittest.mock import patch, mock_open
from src import GPIO

class TestGPIO(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.gpio.subprocess.run')
    def test_write_to_file(self, mock_subprocess, mock_file):
        gpio = GPIO()
        gpio._write_to_file('some_path', 'some_value')
        
        mock_file.assert_called_with('some_path', 'w')
        mock_file().write.assert_called_with('some_value')
    