import speech_recognition as sr
import sounddevice as sd
import numpy as np
import tempfile
import soundfile as sf
from requests_html import HTMLSession
import speak


def spech_to_text(fs=44100):
    r = sr.Recognizer()
    print("Listening...")

    tries = 0
    while True:
        # record a short chunk (adjust duration if needed)
        duration = 5  # seconds
        audio_data = sd.rec(
            int(duration * fs), samplerate=fs, channels=1, dtype="float32"
        )
        sd.wait()

        # save to temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav") as tmpfile:
            sf.write(tmpfile.name, audio_data, fs)
            with sr.AudioFile(tmpfile.name) as source:
                audio = r.record(source)
                try:
                    tries = 0
                    voice_data = r.recognize_google(audio)
                    return voice_data  # stop after successful recognition
                except sr.UnknownValueError:
                    # keep listening until speech is detected
                    tries += 1
                    if tries >= 5:
                        speak.speak("Sorry, please try again")
                        return None
                    continue
                except sr.RequestError:
                    speak.speak("No internet connection, please turn on your internet")
                    return None

spech_to_text()