
# coding: utf-8

# In[1]:


from chatterbot import ChatBot
import speech_recognition
import win32com.client as wincl
import random
from time import sleep
import threading


# In[3]:


bot = ChatBot('Jeffey',
             storage_adapter = 'chatterbot.storage.SQLStorageAdapter',
             database_uri = 'sqlite:///db.sqlite3')    
# The sqlite file is the resultant file of the training modules, so here I am setting it as the chatbot's database

recognizer = speech_recognition.Recognizer()
# setting up way to leverage speech recognition module to convert speech to text
speak = wincl.Dispatch("SAPI.SpVoice") 
# setting up way to leverage win32com.client to convert text to speech
# speech --> text (prompt) --> chatbot --> text (response)


class spot:                     # this is used to pull out an audio file from thread so it can run through the recognizer
    def __init__(self):             
        self.data=[None]
    def put(self,x):
        self.data[0]=x
    def pull(self): 
        return self.data[0]

def listening():                      # visual indication that bot is in listening phase
    for frame in r'-\|/-\|/':
        print('\b', frame, sep='', end='', flush=True)
        sleep(0.2)

def record(que, source):              # pass in spot and source used to record audio
    que.put(recognizer.listen(source))  # put audio file into the spot
queue = spot()
        
with speech_recognition.Microphone() as source:     # sets the device's microphone as the audio input
    while True:
        if __name__ == '__main__':  # start threading: one thread listens to audio while the program runs visual indication
            thread1 = threading.Thread(target=record, args=(queue, source))
            thread1.start()
        print('Listening  ', end='', flush=True)    # prints out 'listening' with visual indication w/o creating a new line
        while threading.Thread.is_alive(thread1):   # while it is recording, the program provides the visual indication
            listening()
        
        
        audio = queue.pull()     # pulls the audio from the spot where the thread put it
        
        try:
            request = recognizer.recognize_google(audio)  # runs the audio through Google's speech-to-text engine
            print('\nYou:', request)                      # bot prints out what it thinks you said
            to_loop=False                                 # speech was recognized, needs to respond
            # print(type(request))
        except:
            to_loop=True                                  # speech was unrecognizable, needs another input                         
            speak.Speak('That is nonsense, try again')
       
        
        
        if not to_loop:
            if "bye" in request or "later" in request:    # if either is in input, ends program by exiting while loop
                speak.Speak("Goodbye")
                break
            
            response = bot.get_response(request)          # based on request, gets response from database
            print('Jeffey:', response)
            speak.Speak(response)
        
        
# Summary: First used threading to listen to user and to visually tell the user we are listening at the same time. 
# Next we send the audio file to Google to convert to text.
# Then we feed text to chatterbot and save response in variable.
# Use another module to convert that text to speech.

