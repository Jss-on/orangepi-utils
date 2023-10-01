# Initialize and set filename
import sys
sys.path.append('.')
from src import Audio
audio = Audio()
audio.setFilename("examples/BabyElephantWalk60.wav")

# Play audio
audio.playAudio()

print(f"Played audio from {audio.filename}")
