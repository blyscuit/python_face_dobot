import bot_burger as bb
import pyttsx3 as tts
import speech_recognition as sr

burger_def = [
    {'name': 'RGB Burger', 'number': ['one', '1'], 'ingredients': ['red', 'green', 'blue']},
    {'name': 'Eco Burger', 'number': ['two', '2'],'ingredients':['pink', 'leaf', 'yellow']},
    {'name': 'Sweet Burger','number': ['three', '3'],'ingredients':['purple', 'blue', 'purple']}
]

engine = tts.init()

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
    
print(take_order())