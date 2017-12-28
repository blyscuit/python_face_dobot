import pyttsx3 as tts
import speech_recognition as sr

engine = tts.init()
r = sr.Recognizer()

while(True):
    print("Say something!")
    engine.say("Say Something")
    engine.runAndWait()
    
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
    engine.say(speech)
    engine.runAndWait()
    