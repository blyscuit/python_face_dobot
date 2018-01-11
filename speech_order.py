import bot_burger as bb
import pyttsx3 as tts
import speech_recognition as sr
import face_recognition
import cv2
import numpy
import queue as queue
from threading import Thread
import time

burger_def = [
    {'name': 'RGB Burger', 'number': ['one', '1'], 'ingredients': ['red', 'green', 'blue']},
    {'name': 'Eco Burger', 'number': ['two', '2'],'ingredients':['pink', 'leaf', 'yellow']},
    {'name': 'Sweet Burger','number': ['three', '3'],'ingredients':['purple', 'blue', 'purple']}
]

engine = tts.init()


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

database_name = ["Barack"]
database_face = [obama_face_encoding]

#should be 300
FACE_SIZE = 300
faceID = 0

currentBurger = None
burgerQuere = []

def speak(sentence):
    print(sentence)
    engine.say(sentence)
    engine.runAndWait()

def listen(keywords):
    r = sr.Recognizer()
    while(True):
        print('listening...')
        with sr.Microphone() as source:
            audio = r.listen(source)
        speech = ""
        try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
            speech = r.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + speech)
            for word in keywords:
                if word in speech:
                    return word
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    #return speech

def take_order():
    #confirmed = False
    order = ''
    while(True):
        speak('Hello, which burger would you like. Just say number one, two or three')
        order = listen(['one', 'two', 'three', '1', '2', '3'])
        speak('You have selected number ' + order)
        speak('Are you sure')
        confirmation = listen(['yes', 'no'])
        if confirmation is 'yes':
            speak('Thank you, your order has been received')
            break
    for burger in burger_def:
        if any(number is order for number in burger['number']):
            return burger
    
#print(take_order())