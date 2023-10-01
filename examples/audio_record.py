# Initialize and set filename
import sys
sys.path.append('.')
from src import Audio
audio = Audio()
audio.setFilename("my_audio.wav")

# Record audio
audio.recordAudio()

print(f"Audio has been recorded to {audio.filename}")
