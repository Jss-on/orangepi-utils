import subprocess
import numpy as np
import os
from scipy.io import wavfile
from python_speech_features import mfcc
import joblib
import time
import sys
from datetime import datetime

sys.path.append(".")
from src import USBStorage, GPIO


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


def led_indicator(pin="PA20", time_interval=1, max_blink=3):
    gpio.pinMode(pin, "out")
    # Blink the LED
    count_blink = 0
    while True:
        # Turn the LED on
        gpio.digitalWrite(pin, 1)
        time.sleep(time_interval)  # Wait for 1 second

        # Turn the LED off
        gpio.digitalWrite(pin, 0)
        time.sleep(time_interval)  # Wait for 1 second

        if count_blink == max_blink:
            count_blink = 0
            break

        count_blink += 1


if __name__ == "__main__":
    # Load the trained model
    usb_storage = USBStorage()
    gpio = GPIO()
    # Setup (this is optional as the pinMode is not strictly necessary for the LEDs)
    gpio.pinMode("green", "out")
    gpio.pinMode("red", "out")
    # model_path = usb_storage.get_file_path("best_audio_classifier_v1.pkl")
    model = joblib.load("best_audio_classifier_v1.pkl")

    # Audio settings
    duration = 10  # 10 seconds
    samplerate = 16000  # 16 kHz
    filename = "temp_audio.wav"  # Temporary audio file name

    count = 0
    while True:
        # Capture audio
        gpio.digitalWrite("green", 1)
        gpio.digitalWrite("red", 1)

        print("Capturing audio...")
        audio_data = capture_audio(duration, samplerate, filename)

        # Extract MFCC features
        mfcc_features = extract_mfcc_features(audio_data, samplerate)

        # Make prediction
        gpio.digitalWrite("green", 0)
        gpio.digitalWrite("red", 0)
        predicted_label = model.predict(mfcc_features)[0]

        if predicted_label == "normal":
            for i in range(10):
                gpio.digitalWrite("green", 0)
                # gpio.digitalWrite("red", 0)
                time.sleep(0.1)
                gpio.digitalWrite("green", 1)
                # gpio.digitalWrite("red", 1)
        else:
            for i in range(10):
                # gpio.digitalWrite("green", 0)
                gpio.digitalWrite("red", 0)
                time.sleep(0.1)
                # gpio.digitalWrite("green", 1)
                gpio.digitalWrite("red", 1)
        # Get confidence level
        predicted_proba = model.predict_proba(mfcc_features)
        confidence = np.max(predicted_proba)  # Take maximum probability as confidence

        print(f"Predicted Label: {predicted_label} with confidence {confidence:.2f}")

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Create the result string with the timestamp
        result = ",".join([timestamp, str(count), predicted_label, str(confidence)])

        usb_storage.append("inference result.txt", result + "\n")

        # gpio.digitalWrite(pin, 0)
        count += 1
        # Wait before capturing the next audio
        time.sleep(1)  # wait for 1 second
