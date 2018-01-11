import face_recognition
import cv2
import numpy
import queue as queue
from threading import Thread
import time
import pyttsx3 as tts
import speech_recognition as sr
import 
    
class dotdict(dict):
# """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
class MyPriorityQueue(queue.PriorityQueue):
    def __init__(self):
        queue.PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        queue.PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    def get(self, *args, **kwargs):
        _, _, item = queue.PriorityQueue.get(self, *args, **kwargs)
        return item



class Ingredient:
    bread = 1
    bacon = 2
    cheese = 3
    beef = 4
    candy = 5
    cake = 6
    lettuce = 7
class Burger:
    hamburger = dotdict({"ingredients":[Ingredient.bread, Ingredient.lettuce, Ingredient.beef, Ingredient.bread], "name":"hamburger", "value":0, "done":False})
    cheeseburger = dotdict({"ingredients":[Ingredient.bread, Ingredient.lettuce, Ingredient.cheese, Ingredient.beef, Ingredient.bread], "name":"cheeseburger", "value":1, "done":False})
    baconburger = dotdict({"ingredients":[Ingredient.bread, Ingredient.bacon, Ingredient.cheese, Ingredient.beef, Ingredient.bread], "name":"baconburger", "value":2, "done":False})
    sweetburger = dotdict({"ingredients":[Ingredient.bread, Ingredient.candy, Ingredient.cake, Ingredient.bread], "name":"sweetburger", "value":3, "done":False})
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

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
# I WILL DO THREAD ROBOT ARM
# _________________________________
# Create thread for robot arm

def do_stuff(q):
    while True:
        try:
            next = q.get()
            print(next[0])
            if next[0] == 0:
                do_robot(q, next)
            
            elif next[0] == 1:
                do_robotserve(q, next)
            else:
                do_bang(q)
        except:
            print("BOMB")
            q.task_done()
    
def do_robot(q, next):
    global burgerQuere
    print("robot making " + (next[1].name))
    time.sleep(5)
    for burger in burgerQuere:
        if burger.done == 0:
            burger.done = 1
            break
#	while True:
    q.task_done()
    print("robot Done")
   
def do_robotserve(q, next):
    global burgerQuere
#	while True:
    print("robot serving " + (next[1].name))
    time.sleep(3)
    q.task_done()
    print("robot Done")
    time.sleep(1)
    
def do_bang(q):
    print("Bang!!")
    q.task_done()

q = MyPriorityQueue()
worker = Thread(target=do_stuff, args=(q,))
worker.setDaemon(True)
worker.start()


def inputLoop():
    global currentBurger
#    print ColorTextExt.PROPMTEXT + "What are you? \n " + "WEREWOLF = 0    SEER = 1    THIEF = 2    VILLAGER = 3 \n " + "VOTE = v[role]    STEAL = t[person][role]    OTHER = p[person][role]" + ColorTextExt.RESET + "\n"
    while 1:
        input_string = input()
        try:
            i = int(float(input_string))
            if i == 1:
                print(Burger.hamburger.name)
                currentBurger = Burger.hamburger
            elif i == 2:
                print(Burger.cheeseburger.name)
                currentBurger = Burger.cheeseburger
            elif i == 3:
                print(Burger.baconburger.name)
                currentBurger = Burger.baconburger
            elif i == 4:
                print(Burger.sweetburger.name)
                currentBurger = Burger.sweetburger
        except:
            print("Input something else")
        

inputor = Thread(target=inputLoop, args=())
inputor.setDaemon(True)
inputor.start()

#engine = tts.init()
r = sr.Recognizer()

#def looking_at_face():
#    global video_capture
#
#    # Load a sample picture and learn how to recognize it.
#    global obama_image
#    global obama_face_encoding
#
#    # Initialize some variables
#    global face_locations
#    global face_encodings
#    global face_names
#    global process_this_frame
#
#    global database_name
#    global database_face
#
#    #should be 300
#    global FACE_SIZE
#    global faceID
#    global process_this_frame
#    
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
                    currentBurger = None
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

#looker = Thread(target=looking_at_face, args=())
#looker.setDaemon(True)
#looker.start()

def listen_hey():
    print("Say something!")
#    engine.say("Say Something")
#    engine.runAndWait()
    
    with sr.Microphone() as source:
        audio = r.listen(source)
    
    speech = ""
    try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
        speech = "Google Speech Recognition thinks you said " + r.recognize_google(audio)
    except sr.UnknownValueError:
        speech = "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        speech = "Could not request results from Google Speech Recognition service; {0}".format(e)
    
    print(speech)
#    engine.say(speech)
#    engine.runAndWait()

#while 1:
#    pass