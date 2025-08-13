import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    audio = r.listen(source)
    voice_data = ""
    voice_data = r.recognize_google(audio)
    print(voice_data)
