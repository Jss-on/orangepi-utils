# Initialize
from src import Audio
audio = Audio()

# Set custom settings
audio.setFilename("custom_audio.wav")
audio.setDuration(10)  # 10 seconds
audio.setRate(22050)   # 22.05 kHz

# Record audio
audio.recordAudio()

print(f"Audio has been recorded to {audio.filename} with duration {audio.duration} seconds and sample rate {audio.rate} Hz")
