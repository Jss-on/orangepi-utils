import subprocess
import os

class Audio:
    def __init__(self, duration=5, rate=44100, format="cd"):
        self.setDuration(duration)
        self.setRate(rate)
        self.setFormat(format)
        self.setFilename("default.wav")
        
    def setFilename(self, filename):
        if not isinstance(filename, str):
            raise ValueError("Filename must be a string.")
        self.filename = filename

    def setDuration(self, duration):
        if not isinstance(duration, (int, float)):
            raise ValueError("Duration must be an integer or float.")
        if duration <= 0:
            raise ValueError("Duration must be greater than zero.")
        self.duration = duration

    def setRate(self, rate):
        if not isinstance(rate, int):
            raise ValueError("Rate must be an integer.")
        if rate <= 0:
            raise ValueError("Rate must be greater than zero.")
        self.rate = rate

    def setFormat(self, format):
        if not isinstance(format, str):
            raise ValueError("Format must be a string.")
        # Additional checks can be included based on the accepted ALSA formats
        self.format = format
        
    def recordAudio(self):
        command = f"arecord -d {self.duration} -f {self.format} -r {self.rate} {self.filename}"
        subprocess.run(command, shell=True)
    
    def playAudio(self):
        command = f"aplay {self.filename}"
        subprocess.run(command, shell=True)

    def getAudioPath(self):
        """
        Returns the full path of the recorded audio file.
        """
        # Assuming that the filename is relative to the current working directory
        current_working_directory = os.getcwd()
        full_path = os.path.join(current_working_directory, self.filename)
        
        return full_path
