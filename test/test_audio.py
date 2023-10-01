import unittest
from unittest.mock import patch
from src import Audio  # Modify this line based on your actual import path

class TestAudio(unittest.TestCase):

    def test_init(self):
        audio = Audio()
        self.assertEqual(audio.duration, 5)
        # ... add more checks for other attributes

    @patch('src.audio.subprocess.run')
    def test_recordAudio(self, mock_subprocess):
        audio = Audio()
        audio.recordAudio()
        
        mock_subprocess.assert_called_with('arecord -d 5 -f cd -r 44100 default.wav', shell=True)
        
    # ... add more test cases for other methods
