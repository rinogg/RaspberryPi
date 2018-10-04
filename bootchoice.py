import time
import subprocess
import datetime
import os
import speech_recognition as sr
import random
from gtts import gTTS

r = sr.Recognizer()
mic = sr.Microphone()
r.energy_threshold = 300

def listenmic():
        
    while True:  
        with mic as source:
           
            beep = subprocess.Popen(["mplayer", '/home/pi/Desktop/BootPyScripts/beep.mp3'], shell = False, stdout=subprocess.PIPE)
            beep = subprocess.Popen(["mplayer", '/home/pi/Desktop/BootPyScripts/beep.mp3'], shell = False, stdout=subprocess.PIPE)
            print ("listening")
            audio = r.listen(source)
##            speak("Processing")
           
            #r.adjust_for_ambient_noise(source)

        
        
        try:
       
            print (r.recognize_google(audio))
            return (r.recognize_google(audio))
        except sr.UnknownValueError:
            speak("Did not understand")
        except sr.RequestError:
            speak ("I can't connect to the A P I. Try again.")
            
            
def silentlistenmic():
    
    while True:  
        with mic as source:
            
            print ("listening")
            audio = r.listen(source, timeout = 3, phrase_time_limit=3)
            r.adjust_for_ambient_noise(source)

        try:
            print("processing")
            print (r.recognize_google(audio))
            return (r.recognize_google(audio))
        except sr.UnknownValueError:
            print ("don't understand, repeating")
            continue
        except sr.RequestError:
            speak ("I can't connect to the A P I. Try again.")


def speak(string):
    
    tts = gTTS(text=string, lang='en')
    tts.save("/home/pi/Desktop/BootPyScripts/audio.mp3")

    process = subprocess.Popen(["mplayer", '/home/pi/Desktop/BootPyScripts/audio.mp3'], shell = False, stdout=subprocess.PIPE)
    process.wait() #search tag modificare1 in subprocess.py wait time changed from 1000 to 500
    os.remove("/home/pi/Desktop/BootPyScripts/audio.mp3")


def radio():
    
    speak("Accessing option one: Radio function.")
    speak("Say - stop or terminate to stop the radio")
    DEVNULL = open(os.devnull, 'wb')
    radiostream = subprocess.Popen(["mplayer", 'http://edge-bauerabsolute-02-gos1.sharp-stream.com/absolute90s.mp3?&'], shell = False, stdout=DEVNULL, stderr=DEVNULL)

    while True:
        try:
            choices = silentlistenmic()
        except NameError:
            speak("Invalid Command")
            print("Invalid Command\n")
            continue
        except SyntaxError:
            speak("Invalid Command")
            print("Invalid Command\n")
            continue

        if "stop" in choices or "terminate" in choices or "stop radio" in choices or "radio" in choices:
            speak("Terminating Radio...")
            radiostream.kill()
            radiostream.terminate()
            
            print("Terminating Radio...\n")
            break
        else:
            speak("Invalid Choice")     
            print("Invalid Choice")   

def telltime():
    now = datetime.datetime.now()
    speak("The time is:" + str(now.hour) + " and" + str(now.minute) + " minutes")
    speak("The date is:" + str(now.year) + " the " + str(now.day) + "th" + " of the " + str(now.month) +"th" )

##BOOT

##speak ("Hello! Please give voice commands only when I'm done talking and after the beep. How may I help?")
##speak ("Moo Yeh Drugn-yah")

while True:

    print ("Select function please:")

                
    try:
        beep = subprocess.Popen(["mplayer", '/home/pi/Desktop/BootPyScripts/beep.mp3'], shell = False, stdout=subprocess.PIPE)
        beep = subprocess.Popen(["mplayer", '/home/pi/Desktop/BootPyScripts/beep.mp3'], shell = False, stdout=subprocess.PIPE)
        choice = listenmic()
        
    except SyntaxError: #for empty input
        speak("Please enter a number")
        continue
    except NameError: #for input that is not int
        speak("Not a number, try again!")
        continue
    
    if "radio" in choice or "music" in choice or "Radio" in choice:
        radio()
    
    elif "time" in choice or "date" in choice:
        telltime()
    
    elif "what can you do" in choice or "what can" in choice or "you do" in choice or "you too" in choice:
        speak ("I can play the radio or tell you the time. Simply ask for it.")
    
    elif "help" in choice or "yelp" in choice or "welp" in choice:
        speak ("Make sure your voice is clear and the keyword is included in a sentence. "
        +"Say -- please tell me the time - instead of just time. "
        +"Please give commands only when I am done talking and after the beep. "
        +"I can play the radio or tell you the time. Simply ask for it.")
    
    elif "hello" in choice or "hi" in choice:
        speak("Hello")
    
    elif "how are you" in choice or "are you" in choice or "you" in choice:
        speak ("I am fine, thank you!")
        
    else:
        speak("Invalid Choice")            
        print("Invalid choice.\n")
    

print("EOF: SHOULD NOT HAPPEN")



