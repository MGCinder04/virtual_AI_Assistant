import datetime
import webbrowser
import os
import wikipedia
import pyjokes
import glob
import speak


def open_app(app_name):
    app_name = app_name.lower()

    # Try opening directly (works if in PATH)
    try:
        os.system(f"start {app_name}")
        return True
    except:
        pass

    # Fallback: search in Start Menu and Desktop
    possible_paths = [
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expanduser("~/Desktop"),
    ]

    for path in possible_paths:
        for file in glob.glob(path + "/**/*.lnk", recursive=True):
            if app_name in os.path.basename(file).lower():
                os.startfile(file)  # works for shortcuts
                return True
    return False


def Action(send):
    data_btn = send.lower()

    # Greetings
    if "your name" in data_btn:
        speak.speak("My name is Virtual Assistant")
        return "My name is Virtual Assistant"

    elif "hello" in data_btn or "hi" in data_btn:
        speak.speak("Hello! How can I help you today?")
        return "Hello! How can I help you today?"

    # Date & Time
    elif "time" in data_btn:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak.speak(f"The time is {now}")
        return now

    elif "date" in data_btn or "day" in data_btn:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak.speak(f"Today is {today}")
        return today

    # Web browsing
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

    # Wikipedia
    elif "who is" in data_btn or "what is" in data_btn:
        query = data_btn.replace("who is", "").replace("what is", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=2)
            speak.speak(summary)
            return summary
        except:
            speak.speak("Sorry, I couldn't find that on Wikipedia.")
            return "No result found"

    # Fun
    elif "joke" in data_btn:
        joke = pyjokes.get_joke()
        speak.speak(joke)
        return joke

    # Generalized App Opening with fallback
    elif "open" in data_btn:
        app = data_btn.replace("open", "").strip()
        if open_app(app):
            speak.speak(f"Opening {app}")
            return f"Opening {app}"
        else:
            speak.speak(f"Sorry, I couldn't find {app}")
            return f"Could not open {app}"

    # Exit
    elif "shutdown" in data_btn or "quit" in data_btn:
        speak.speak("Okay, shutting down. Goodbye!")
        exit()

    else:
        speak.speak("I'm not sure how to help with that yet.")
        return "Command not recognized"
