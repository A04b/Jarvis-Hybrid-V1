import speech_recognition as sr
import pyttsx3
import psutil
import datetime
import os
import webbrowser
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv() #searches .env and Loads its contents into memory
api_key = os.getenv("GEMINI_API_KEY")   # Grab key from the environment variables
genai.configure(api_key=api_key) #congifuring AI with my key

def get_ai_response(prompt):
   try:
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        response = model.generate_content(f"Answer this in short: {prompt}")
        return response.text  
   except Exception as e:
        print(f"Error with AI Brain: {e}")
        return "My brain is currently offline!"

#OUTPUT MODULE
def speak(text):
    print(f"JARVIS: {text}")

    #Initialize mouth
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 190) 

    engine.say(text)
    engine.runAndWait()

    del engine

#INPUT MODULE(ears initialization)
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        # helps JARVIS ignore background noise
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language= 'en-in')
        print(f"User said: {query}\n")
    except Exception:
        print("I didn't catch that. Could you please repeat?")
        return "None"
    return query.lower()
  

#CONTROL FLOW
if __name__ == "__main__":
    #starting
    speak("Hello, I am online. How can I assist you today?")

    print("Choose Mode: [1]Voice Mode | [2]Text Mode")
    mode = input("Enter mode number(1 or 2): ")
    
    while True:
        if mode == "1":
            user_input = take_command()
        else:
            user_input = input("Enter your command(type): ").lower()

        if user_input == "none" or user_input == "":
            continue

        if "hey" in user_input or "hi" in user_input:
            speak("Hey there, I'm listening.")

        elif "your name" in user_input:
            speak("I am Jarvis, your personal desktop assistant.")

        #tells current time
        elif "time" in user_input:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Current time is {strTime}")

        #opens google in default browser
        elif "open google" in user_input:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")

        #opens chrome browser
        elif "open chrome" in user_input:
            speak("Opening Chrome.")
            os.system("chrome.exe")

        #opens vs code
        elif "open code editor" in user_input or "open vs code" in user_input:
            speak("Opening VS Code.")
            os.system("code.exe")

        #opens current folder containing 'notes'
        elif "open notes" in user_input:
            current_dir = os.getcwd()
            notes_path = os.path.join(current_dir, "notes")
            if os.path.exists(notes_path):
                speak("Opening your folder")
                os.startfile(notes_path)
            else:
                speak("Sorry, I couldn't find your notes folder.")

        #searches the query on google
        elif "search for" in user_input:
            search_query = user_input.replace("search for","").strip()
            speak(f"Searching for {search_query} on Google.")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
        
        #shows battery percentage
        elif "battery" in user_input:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                speak(f"Battery is at {percent} percent.")
            
        #end command
        elif "exit" in user_input or "stop" in user_input:
            speak("Goodbye! Shutting down systems.")
            break

        #GenAI response for other queries
        elif user_input != "None":
            speak("Thinking...")
            ai_response = get_ai_response(user_input)
            speak(ai_response)
