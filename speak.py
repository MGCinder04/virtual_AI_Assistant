import pyttsx3

_engine = pyttsx3.init()
_rate = _engine.getProperty("rate")
_engine.setProperty("rate", _rate - 20)


def speak(text: str):
    if not text:
        return
    _engine.say(text)
    _engine.runAndWait()


def set_rate(delta: int):
    r = _engine.getProperty("rate")
    _engine.setProperty("rate", max(80, min(300, r + delta)))


def stop():
    _engine.stop()
