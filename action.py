import datetime
import webbrowser
import os
import wikipedia
import pyjokes
import glob
import speak
import ctypes
import pygetwindow as gw
import pyautogui
import requests
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc


def open_app(app_name):
    app_name = app_name.lower()

    try:
        os.system(f"start {app_name}")
        return True
    except:
        pass

    possible_paths = [
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expanduser("~/Desktop"),
    ]

    for path in possible_paths:
        for file in glob.glob(path + "/**/*.lnk", recursive=True):
            if app_name in os.path.basename(file).lower():
                os.startfile(file)
                return True
    return False


def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))


def Action(send):
    if send is None:
        speak.speak("I'm not sure how to help with that yet.")
        return "Command not recognized"
    data_btn = send.lower()

    if "your name" in data_btn:
        speak.speak("My name is Virtual Assistant")
        return "My name is Virtual Assistant"

    elif "hello" in data_btn or "hey" in data_btn:
        speak.speak("Hello! How can I help you today?")
        return "Hello! How can I help you today?"

    elif "time" in data_btn:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak.speak(f"The time is {now}")
        return now

    elif "date" in data_btn or "day" in data_btn:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak.speak(f"Today is {today}")
        return today

    elif "increase brightness" in data_btn:
        try:
            # Extract number if given
            parts = data_btn.split()
            step = next((int(p) for p in parts if p.isdigit()), 10)  # default 10
            current = sbc.get_brightness(display=0)[0]
            new_level = min(100, current + step)
            sbc.set_brightness(new_level, display=0)
            speak.speak(f"Increasing brightness to {new_level} percent")
            return f"Brightness set to {new_level}%"
        except:
            return "Error adjusting brightness"

    elif "decrease brightness" in data_btn:
        try:
            parts = data_btn.split()
            step = next((int(p) for p in parts if p.isdigit()), 10)  # default 10
            current = sbc.get_brightness(display=0)[0]
            new_level = max(0, current - step)
            sbc.set_brightness(new_level, display=0)
            speak.speak(f"Decreasing brightness to {new_level} percent")
            return f"Brightness set to {new_level}%"
        except:
            return "Error adjusting brightness"

    elif "set brightness" in data_btn:
        try:
            parts = data_btn.split()
            value = next((int(p) for p in parts if p.isdigit()), None)
            if value is not None:
                value = max(0, min(100, value))  # clamp 0–100
                sbc.set_brightness(value, display=0)
                speak.speak(f"Brightness set to {value} percent")
                return f"Brightness set to {value}%"
            else:
                speak.speak("Please specify a brightness level")
                return "No brightness specified"
        except:
            return "Error setting brightness"

    elif "increase volume" in data_btn:
        vol = get_volume_interface()
        try:
            # Extract number if given
            parts = data_btn.split()
            step = next((int(p) for p in parts if p.isdigit()), 10)  # default 10
            current = int(vol.GetMasterVolumeLevelScalar() * 100)
            new_level = min(100, current + step)
            vol.SetMasterVolumeLevelScalar(new_level / 100, None)
            speak.speak(f"Increasing volume to {new_level} percent")
            return f"Volume set to {new_level}%"
        except:
            return "Error adjusting volume"

    elif "decrease volume" in data_btn:
        vol = get_volume_interface()
        try:
            # Extract number if given
            parts = data_btn.split()
            step = next((int(p) for p in parts if p.isdigit()), 10)  # default 10
            current = int(vol.GetMasterVolumeLevelScalar() * 100)
            new_level = max(0, current - step)
            vol.SetMasterVolumeLevelScalar(new_level / 100, None)
            speak.speak(f"Decreasing volume to {new_level} percent")
            return f"Volume set to {new_level}%"
        except:
            return "Error adjusting volume"

    elif "set volume" in data_btn:
        vol = get_volume_interface()
        try:
            # Extract number
            parts = data_btn.split()
            value = next((int(p) for p in parts if p.isdigit()), None)
            if value is not None:
                value = max(0, min(100, value))  # clamp 0–100
                vol.SetMasterVolumeLevelScalar(value / 100, None)
                speak.speak(f"Volume set to {value} percent")
                return f"Volume set to {value}%"
            else:
                speak.speak("Please specify a volume level")
                return "No volume specified"
        except:
            return "Error setting volume"

    elif "mute" in data_btn:
        os.system("nircmd.exe mutesysvolume 1")
        speak.speak("Muted")
        return "Muted"

    elif "unmute" in data_btn:
        os.system("nircmd.exe mutesysvolume 0")
        speak.speak("Unmuted")
        return "Unmuted"

    elif (
        "play song" in data_btn
        or "song" in data_btn
        or "songs" in data_btn
        or "play songs" in data_btn
        or "music" in data_btn
        or "play music" in data_btn
        or "musics" in data_btn
        or "play musics" in data_btn
    ):
        query = data_btn.replace("play song", "").strip()
        if query:
            url = f"https://music.youtube.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            speak.speak(f"Playing {query} on YouTube Music")
            return f"Playing {query} on YouTube Music"
        else:
            webbrowser.open("https://music.youtube.com/")
            speak.speak("Opening YouTube Music")
            return "Opening YouTube Music"

    elif "open google" in data_btn:
        webbrowser.open("https://google.com")
        speak.speak("Opening Google")
        return "Opening Google"

    elif "open youtube" in data_btn:
        webbrowser.open("https://youtube.com")
        speak.speak("Opening YouTube")
        return "Opening YouTube"

    elif "search" in data_btn:
        query = data_btn.replace("search", "").strip()
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        speak.speak(f"Here are results for {query}")
        return f"Searched: {query}"

    elif "who is" in data_btn or "what is" in data_btn:
        query = data_btn.replace("who is", "").replace("what is", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=2)
            speak.speak(summary)
            return summary
        except:
            speak.speak("Sorry, I couldn't find that on Wikipedia.")
            return "No result found"

    elif "joke" in data_btn:
        joke = pyjokes.get_joke()
        speak.speak(joke)
        return joke

    elif "open" in data_btn:
        app = data_btn.replace("open", "").strip()
        if open_app(app):
            speak.speak(f"Opening {app}")
            return f"Opening {app}"
        else:
            speak.speak(f"Sorry, I couldn't find {app}")
            return f"Could not open {app}"

    elif "exit" in data_btn or "quit" in data_btn:
        speak.speak("Okay, Goodbye!")
        return "Okay, Goodbye!"
        exit()

    elif "sleep" in data_btn:
        speak.speak("Putting PC to sleep")
        ctypes.windll.powrprof.SetSuspendState(0, 1, 0)
        return "PC is going to sleep"

    elif "restart" in data_btn:
        speak.speak("Restarting PC")
        os.system("shutdown /r /t 1")
        return "Restarting PC"

    elif "calculate" in data_btn:
        try:
            expr = data_btn.replace("calculate", "").strip()
            result = eval(expr)
            speak.speak(f"The result is {result}")
            return result
        except:
            speak.speak("Sorry, I couldn't calculate that")
            return "Calculation error"

    elif "screenshot" in data_btn:
        filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pyautogui.screenshot(filename)
        speak.speak("Screenshot taken")
        return f"Screenshot saved as {filename}"

    elif "shutdown" in data_btn:
        speak.speak("Shutting down PC")
        os.system("shutdown /s /t 1")
        return "Shutting down PC"

    elif "close all windows" in data_btn:
        speak.speak("Closing all open windows")
        for window in gw.getAllTitles():
            try:
                gw.getWindowsWithTitle(window)[0].close()
            except:
                pass
        return "Closed all windows"

    elif "minimize all windows" in data_btn:
        speak.speak("Minimizing all open windows")
        for window in gw.getAllWindows():
            try:
                window.minimize()
            except:
                pass
        return "Minimized all windows"

    elif "weather" in data_btn:
        api_key = "63fc809576ac39941ca7cce0aac40205"

        city = data_btn.replace("weather", "").replace("in", "").strip()
        if not city:
            city = "Kanpur"

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()

        if response.get("main"):
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            result = f"The weather in {city} is {desc} with {temp} degrees Celsius"
            speak.speak(result)
            return result
        else:
            speak.speak("Sorry, I couldn't fetch the weather right now.")
            return "Weather data not available"

    else:
        speak.speak("I'm not sure how to help with that yet.")
        return "Command not recognized"
