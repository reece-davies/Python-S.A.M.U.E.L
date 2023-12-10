# AI virtual assistant, following the guide: https://www.activestate.com/blog/how-to-build-a-digital-virtual-assistant-in-python/
# Speech didn't work too well initially. Changed that bit of code
# S.A.M.U.E.L (Simple Assistant Made Under Endless Lockdown)

import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS   # Documentation on Google Text to Speech
import requests, json

# pip install SpeechRecognition
# pip install gTTS
# pip install PyAudio

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening...")
        audio = r.listen(source)

    data = ""
    try:
        data = r.recognize_google(audio)
        print("You said: ", data)
    except sr.UnknownValueError:
        print("Google Speech Recognition did not understand audio")
    except sr.RequestError:
        print("Request failed: {0}".format(e))
    return data

def respond(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save('speech.mp3')
    #os.system('mpg321 speech.mp3')     # Default one from tutorial (doesn't work)
    #os.system('mpyg321 speech.mp3')    # Doesn't work either
    #os.system('start speech.mp3')      # Solution stated in (not complete fix): https://stackoverflow.com/questions/40811540/gtts-google-text-to-speech-error-audio-gets-saved-but-does-not-play-automatic

    # Pygame mixer (when it works, speech is very slow and drunk-like)
    #from pygame import mixer
    #for line in audioString.splitlines():
    #    text_to_speech = gTTS(text=audioString, lang='en-uk')
    #    text_to_speech.save('speech.mp3')
    #    mixer.init()
    #    mixer.music.load("speech.mp3")
    #    mixer.music.play()

    # Playsound (requires 'pip install playsound') (WORKS!)
    from playsound import playsound
    playsound('speech.mp3')
    os.remove('speech.mp3')

    # Simpleaudio (requires 'pip install simpleaudio') (doesn't work)
    #import simpleaudio as sa
    #filename = 'speech.mp3'
    #wave_obj = sa.WaveObject.from_wave_file(filename)
    #play_obj = wave_obj.play()
    #play_obj.wait_done()  # Wait until sound has finished playing

    # Winsound
    #import winsound
    #filename = 'speech.wav'
    #winsound.PlaySound(filename, winsound.SND_FILENAME)

    # Other solutions can be found here: https://realpython.com/playing-and-recording-sound-python/


def digital_assistant(data):
    listening = True

    if "hi" in data or "hello" in data:
        respond("Hello")

    if "how are you" in data or "how you doing" in data or "how are you doing" in data:
        respond("I am well thanks")

    if "what time is it" in data or "what is the time" in data:
        respond(ctime())

    if "where is" in data:
        data = data.split(" ")
        location_url = "https://www.google.co.uk/maps/place/" + str(data[2])
        respond("Processing location " + data[2])
        #maps_arg = '/usr/bin/open -a "/Applications/Google Chrome.app" ' + location_url # For linux machines
        #os.system(maps_arg)

        import webbrowser  # https://pythonexamples.org/python-open-url-in-chrome-browser/
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"))
        webbrowser.get('chrome').open(location_url)

    if "what is the weather in" in data:
        api_key = "de619183aa4c7a8734a9d2e0d6c4fb55"
        weather_url = "http://api.openweathermap.org/data/2.5/weather?"
        data = data.split(" ")
        location = str(data[5])
        url = weather_url + "appid=" + api_key + "&q=" + location 
        js = requests.get(url).json() 
        
        if js["cod"] != "404": 
            weather = js["main"] 
            temp = weather["temp"] 
            hum = weather["humidity"] 
            desc = js["weather"][0]["description"]
            resp_string = " The temperature in Kelvin is " + str(temp) + " The humidity is " + str(hum) + " and The weather description is "+ str(desc)
            respond(resp_string)
        else: 
            respond("City Not Found")

    if "what is" in data: # or "who is" in data
        import wptools
        #so = wptools.page('Stack Overflow').get_parse()
        #infobox = so.data['infobox']
        #print(infobox)

        data = data.split(" ")
        query = str(data[2])

        #page = wptools.page('Gandhi')
        page = wptools.page(str(query))
        page.get_query()
        print(page.data['description'])

        response = str(query) + " is " + page.data['description']
        respond(response)

    
    if "stop listening" in data or "shut down" in data or "power off" in data or "turn off" in data:
        listening = False
        respond("Okay. I will stop. Good bye")
        print('Listening stopped')
        return listening

    return listening

time.sleep(2)
respond("Hello Reece. What can I do for you?")
listening = True
while listening == True:
    data = listen()
    listening = digital_assistant(data)



# I have finished the online guide. Next things to do
# 1. Make name (DONE)
# 2. Fix weather json error (DONE)
# 3. Consider what APIs can be implemeted into this software (https://dev.to/kgcodes/9-free-cool-web-apis-to-use-in-your-next-project-16f1)
# 4. Implement chatbot for better communication, possibly with wit.ai (https://wit.ai/)
# 5. Allow for "what is" searches with GET wikipedia infobox using API (https://stackoverflow.com/questions/3312346/how-to-get-the-infobox-data-from-wikipedia) + (https://github.com/siznax/wptools)
#    ^ Split into "what is" and "who is"