import subprocess
import numpy as np
import os
from scipy.io import wavfile
from python_speech_features import mfcc
import joblib
import time
import sys

sys.path.append(".")
from src import USBStorage


# Function to capture audio using native ALSA command
def capture_audio(duration, samplerate, filename):
    command = (
        f"arecord -D hw:0,0 -d {duration} -f S16_LE -r {samplerate} -c1 {filename}"
    )
    subprocess.call(command, shell=True)
    samplerate, audio_data = wavfile.read(filename)
    os.remove(filename)  # Remove the temporary audio file
    return audio_data


# Function to extract MFCC features
def extract_mfcc_features(audio_data, sample_rate=16000):
    mfcc_features = mfcc(audio_data, sample_rate)
    return np.mean(mfcc_features, axis=0).reshape(1, -1)


if __name__ == "__main__":
    # Load the trained model
    usb_storage = USBStorage()
    # model_path = usb_storage.get_file_path("best_audio_classifier_v1.pkl")
    model = joblib.load("examples/best_audio_classifier_v1.pkl")

    # Audio settings
    duration = 10  # 10 seconds
    samplerate = 16000  # 16 kHz
    filename = "temp_audio.wav"  # Temporary audio file name

    count = 0
    while True:
        # Capture audio
        print("Capturing audio...")
        audio_data = capture_audio(duration, samplerate, filename)

        # Extract MFCC features
        mfcc_features = extract_mfcc_features(audio_data, samplerate)

        # Make prediction
        predicted_label = model.predict(mfcc_features)[0]

        # Get confidence level
        predicted_proba = model.predict_proba(mfcc_features)
        confidence = np.max(predicted_proba)  # Take maximum probability as confidence

        print(f"Predicted Label: {predicted_label} with confidence {confidence:.2f}")

        # Wait before capturing the next audio
        time.sleep(1)  # wait for 1 second
