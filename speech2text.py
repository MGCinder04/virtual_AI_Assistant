import speech_recognition as sr
import sounddevice as sd
import numpy as np
import tempfile
import soundfile as sf
from requests_html import HTMLSession
import speak


def speech2text(fs=44100):
    r = sr.Recognizer()
    speak.speak("listening...")

    tries = 0
    while True:
        # record a short chunk (adjust duration if needed)
        duration = 3  # seconds
        audio_data = sd.rec(
            int(duration * fs), samplerate=fs, channels=1, dtype="float32"
        )
        sd.wait()

        # save to temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            tmpfile_name = tmpfile.name

        sf.write(tmpfile_name, audio_data, fs)

        with sr.AudioFile(tmpfile_name) as source:
            audio = r.record(source)

            try:
                voice_data = r.recognize_google(audio)
                print(voice_data)
                tries = 0
                return voice_data  # stop after successful recognition
            except sr.UnknownValueError:
                # keep listening until speech is detected
                speak.speak("Sorry, please try again")
                tries += 1
                if tries > 2:
                    return None
                continue
            except sr.RequestError:
                speak.speak("No internet connection, please turn on your internet")
                return None
