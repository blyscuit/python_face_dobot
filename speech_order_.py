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
    
currentBurger = take_order()
bb.make_burger(currentBurger['ingredients'])
   
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.face_distance(database_face, face_encoding)
            name = "Unknown"
#            print(match)
            if min(match) <= 0.39: #or 0.40
                matchIndex = numpy.where(match==min(match)) 
                name = database_name[matchIndex[0][0]]
                if burgerQuere[matchIndex[0][0]-1].done == 1:
                    q.put((1,burgerQuere[matchIndex[0][0]-1]),0)
                    burgerQuere[matchIndex[0][0]-1].done = 2
            elif min(match) >= 0.53:
#                new_face_encoding = face_recognition.face_encodings(frame)[0]
            
                if currentBurger != None:
                    database_face.append(face_encoding)
                    database_name.append('%s Person %d' % (currentBurger.name,faceID,))
                    faceID += 1
                    q.put((0,currentBurger),1)
                    burgerQuere.append(currentBurger)
                    bb.make_burger(currentBurger['ingredients'])
#                    currentBurger = None
#                not in database

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        
        if right - left >= FACE_SIZE :

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
            #Do checking face size here

    # Display the resulting image
    

        cv2.imshow('Video', frame)
    
    

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
