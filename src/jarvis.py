import speech_recognition as sr
import pyttsx3 as tts
import datetime
import wikipedia
import webbrowser
import pyjokes

WIKIPEDIA_TRIGGERS = ("wikipedia", "wikipidia", "wiki pedia")


def speak(text: str):
    print(f"Jarvis:{text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        print("The engine didn't responded")


def greet_user():
    speak("Hi")
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("MY name is Jarvis")
    speak("How can i help you?")


def sr_init() -> sr.Recognizer:
    r = sr.Recognizer()
    r.pause_threshold = 1.2
    r.non_speaking_duration = 0.5
    return r


def run_assistant(r):

    user_mode = input(speak("Do you want to type or talk?"))

    while True:

        if user_mode.lower() == "talk":
            query = voice_capture(r).strip().lower()
        else:
            query = input("Enter you command : ")

        if not query:
            continue

        if any(trigger in query for trigger in WIKIPEDIA_TRIGGERS):
            speak("Searching Wikipedia...")
            for trigger in WIKIPEDIA_TRIGGERS:
                query = query.replace(trigger, "")
            query = query.strip()

            if not query:
                speak("Please tell me the topic to search on Wikipedia.")
                continue

            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia:")
                speak(result)
            except:
                speak("Sorry, I couldn't find anything.")

        elif "open youtube" in query:
            speak("Opening YouTube...")
            webbrowser.open("https://www.youtube.com/")

        elif "open google" in query:
            speak("Opening Google...")
            webbrowser.open("https://www.google.com/")

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {strTime}")

        elif "joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "exit" in query or "bye" in query:
            speak("Goodbye! Have a nice day!")
            break

        else:
            speak("Sorry, I didn't understand that. Try again.")


def voice_capture(r):
    text = ""
    with sr.Microphone() as source:
        print("Calibrating microphone... stay quiet.")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Talk:")
        audio_text = r.listen(source)
        print("Finished listening.")
        try:
            text = r.recognize_google(audio_text)
            print(f"You said: {text}")
        except:
            speak("Iam sorry! i didn't catch that! ")

        return text


try:
    engine = tts.init()
except:
    print("Engine creation failed")

r = sr_init()

greet_user()

run_assistant(r)
