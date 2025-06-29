import speech_recognition as sr
from gtts import gTTS
import os


class VoiceInterface:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                return self.recognizer.recognize_google(audio).lower()
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                return None

    def speak(self, text):
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        os.system("start response.mp3")