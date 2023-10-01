# Initialize and set filename
from src import Audio
audio = Audio()
audio.setFilename("my_audio.wav")

# Play audio
audio.playAudio()

print(f"Played audio from {audio.filename}")
