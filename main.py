import ctypes
import smtplib
import bs4
import pyjokes as pyjokes
import pyttsx3
import pytz as pytz
import speech_recognition as sr
import datetime
import webbrowser
import wikipedia
import os
import random
import pywhatkit
import subprocess
import requests
import winshell as winshell
from requests.api import get
from time import time
from flask import Flask, request

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

def speak(audio):
    engine.say(audio)
    print(f"Jarvis: {audio}")
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if (hour >=0 and hour<12):
        a = "Good morning Sir", "Hello, Good morning sir", "A very good morning sir", "Sir, A very Happy morning !!", "Wish you a pleasant morning sir"
        speak(random.choice(a))
    elif (hour>=12 and hour<18):
        b = "Good Afternoon Sir", "Hello sir, Good afternoon", "Sir, Good afternoon"
        speak(random.choice(b))
    elif (hour>=18 and hour<24):
        c = "Good Evening Sir", "Happy evening sir", "Good evening Harshal sir"
        speak(random.choice(c))
    else:
        d = "Good night Sir", "Have a good sleep night sir", "Take care Good night sir"
        speak(random.choice(d))
    wl = "Jarvis at your service sir. Please tell me what shall I do for you", "How can I help you sir ?", "Jarvis ready to work. what can I do for you sir ?", "What can I do for you?"
    speak(random.choice(wl))

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=60, phrase_time_limit=5)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"Your Command : {query}\n")

    except Exception as e:
        error = "I don’t understand you sir.", "Sorry I could not listen", "Please try to say again...!!"
        speak(random.choice(error))
        return "none"
    return query

if __name__ == "__main__":
    wishme()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query or 'search wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(result)

        elif 'play' in query or 'youtube' in query:
            query = query.replace("video", "")
            query = query.replace("on youtube", "")
            query = query.replace("youtube", "")
            query = query.replace("play", "")
            string = query.split()
            search = ""
            for i in string:
                search += i
                search += "+"
            webbrowser.open(f"https://www.youtube.com/results?search_query={search}")
            speak(f"Playing {query} on youtube")

        elif 'jarvis' in query or 'who are you' in query:
            who = "I'm jarvis your personal assistant", "Jarvis at your service sir !! How can I help you."
            speak(random.choice(who))

        elif 'search' in query or 'google' in query:
            query = query.replace("search", "")
            query = query.replace("on google", "")
            query = query.replace("open", "")
            query = query.replace("google", "")
            string = query.split()
            search = ""
            for i in string:
                search += i
                search += "+"
            webbrowser.open(f"https://www.google.com/search?q={search}&oq={search}&aqs="
                            f"chrome.2.69i57j0i10i131i433j0i10i433l3j0i10l2j46i10i175i199j0i10i433j0i10."
                            f"2660j0j15&sourceid=chrome&ie=UTF-8")
            speak(f"Searching {query}")

        elif 'open notepad' in query:
            npath = "C:\\WINDOWS\\system32\\notepad.exe"
            os.startfile(npath)
            speak("Opening Notepad..")

        elif 'open command prompt' in query or 'open cmd' in query:
            os.system("start cmd")
            speak("Opening Command Prompt..")

        elif 'reason for you' in query or 'purpose for you' in query:
            speak("I was created as a mini project by sir Harshal")

        elif "who i am" in query or 'who am i' in query:
            speak("If you talk then definitely your human !! or robot?")

        elif 'empty recycle bin' in query:
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
            speak("Recycle Bin Recycled")

        # This will lock your window work itself safely
        elif 'lock window' in query:
            speak("locking the device")
            ctypes.windll.user32.LockWorkStation()

        # This will shut down your window work itself safely
        elif 'shutdown system' in query:
            shut = "Hold On a Sec ! Your system is on its way to shut down", "Jarvis shutting down system.", "Don't be panic, it will safely shut down"
            speak(random.choice(shut))
            subprocess.call('shutdown / p /f')

        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'the date' in query:
            date = datetime.datetime.now(tz = pytz.timezone('Asia/kolkata'))
            speak(date.strftime("Sir, the date is %d %B %A, %Y"))

        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")

        elif 'exit' in query or 'terminate yourself' in query:
            exit_msg = "Thanks for giving me your time", "Anytime sir, Jarvis is available for your service", "Please call me when you need !"
            speak(random.choice(exit_msg))
            exit()

        elif 'joke' in query or 'tell me a joke' in query:
            speak(pyjokes.get_joke())

        elif 'thank you' in query:
            thanks = "It's my pleasure", "Your Welcome!!", "Thanks for operating me"
            speak(random.choice(thanks))

        elif "write a note" in query:
            speak("What should I write, sir?")
            note = takeCommand()
            file = open('jarvis.txt', 'w')
            speak("Sir, Should i include date and time")
            snfm = takeCommand()
            if 'yes' in snfm or 'sure' in snfm:
                file.write(" ")
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(note)
                speak("Sir, file saved with time")
            if 'no' in snfm or 'not' in snfm:
                file.write(note)
                speak("Sir, file not saved with time")

        elif "show note" in query:
            speak("Showing Notes")
            file = open("jarvis.txt", "r")
            print(file.read())
            speak(file.read(6))

        elif "temperature" in query or "what is the" in query:
            query = takeCommand().lower()
            Query = query.replace("what is the", "")
            search = Query
            url = (f"https://www.google.com/search?q={search}&oq={search}&aqs="
                            f"chrome.2.69i57j0i10i131i433j0i10i433l3j0i10l2j46i10i175i199j0i10i433j0i10."
                            f"2660j0j15&sourceid=chrome&ie=UTF-8")
            r = requests.get(url)
            data = bs4.BeautifulSoup(r.text, "html.parser")
            temp = data.find("div", class_ = "BNeawe").text
            speak(f"Current {search} is {temp}")

        elif 'open camera' in query:
            subprocess.run('start microsoft.windows.camera:', shell=True)
            speak("Opening camera..")

