 import subprocess

def speak(text):
    print("Jarvis:", text)
    subprocess.run(['termux-tts-speak', text])
import subprocess
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import requests
import json

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def speak(text):
    print("Jarvis:", text)
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except Exception:
        speak("Sorry, I did not get that.")
        return ""

def tell_time():
    now = datetime.datetime.now()
    return now.strftime("The time is %H:%M")

def open_website(site):
    url = f"https://{site}"
    webbrowser.open(url)
    speak(f"Opening {site}")

def search_wikipedia(query):
    speak("Searching Wikipedia...")
    try:
        results = wikipedia.summary(query, sentences=2)
        speak(results)
    except Exception:
        speak("I couldn't find anything on Wikipedia.")

def call_number(number):
    speak(f"Calling {number}")
    os.system(f"termux-telephony-call {number}")

def send_sms(number, message):
    speak(f"Sending SMS to {number}")
    # Send SMS using Termux API
    os.system(f'termux-sms-send -n {number} "{message}"')

def get_weather(city):
    # Using OpenWeatherMap API (you need your own API key)
    API_KEY = 'your_openweathermap_api_key_here'
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        speak(f"The temperature in {city} is {temp} degrees Celsius with {desc}")
    else:
        speak("I couldn't get the weather for that location.")

def tell_joke():
    # Simple hardcoded joke
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything.",
        "Why did the math book look sad? Because it had too many problems.",
        "Why did the scarecrow win an award? Because he was outstanding in his field."
    ]
    import random
    speak(random.choice(jokes))

def main():
    speak("Hello! Jarvis here. How can I help you?")
    while True:
        command = listen_command()

        if not command:
            continue

        if "time" in command:
            speak(tell_time())
        elif "open" in command:
            site = command.replace("open", "").strip()
            if site:
                open_website(site)
            else:
                speak("Please tell me the website to open.")
        elif "wikipedia" in command:
            topic = command.replace("wikipedia", "").strip()
            if topic:
                search_wikipedia(topic)
            else:
                speak("Please specify a topic for Wikipedia.")
        elif "call" in command:
            # Extract number (naive approach)
            number = ''.join(filter(str.isdigit, command))
            if number:
                call_number(number)
            else:
                speak("Please say the number to call.")
        elif "send sms" in command or "send message" in command:
            speak("To whom should I send the message?")
            number = listen_command()
            speak("What is the message?")
            message = listen_command()
            if number and message:
                send_sms(number, message)
            else:
                speak("Failed to get the number or message.")
        elif "weather" in command:
            speak("Which city?")
            city = listen_command()
            if city:
                get_weather(city)
            else:
                speak("Please tell me the city name.")
        elif "joke" in command:
            tell_joke()
        elif "exit" in command or "quit" in command or "stop" in command:
            speak("Goodbye!")
            break
        else:
            speak("I can't do that yet. Try something else!")

if __name__ == "__main__":
    main()
