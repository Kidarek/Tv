import concurrent.futures
import speech_recognition as sr
from pylgtv import WebOsClient
from wakeonlan import send_magic_packet
import time
import pyttsx3
from selenium import webdriver

wc = WebOsClient('192.168.1.134')
mic = sr.Microphone(device_index=1)
r = sr.Recognizer()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


class Television():
    powered = False
    paused = False

    def power_on(self):
        if self.powered:
            return
        self.powered = True
        send_magic_packet('30:B1:B5:19:39:14')
        time.sleep(2)

    def power_off(self):
        self.powered = False
        try:
            wc.power_off()
        except concurrent.futures._base.TimeoutError:
            pass

    def start_app(self, app_name):
        self.power_on()
        wc.launch_app(app_name)

    def pause(self):
        self.power_on()
        if self.paused:
            return
        wc.pause()

    def play(self):
        self.power_on()
        wc.play()
        time.sleep(.5)


class Controller():
    current_device = ''
    tv = Television()

    def audio_command(self, audio_txt):
        print(audio_txt)
        self.set_device(audio_txt)
        if self.current_device == 'TV':
            if 'off' in audio_txt:
                self.tv.power_off()
            else:
                apps = [['netflix', 'netflix'], ['disney', 'com.disney.disneyplus-prod']]
                for app in apps:
                    if app[0] in audio_txt:
                        self.tv.start_app(app[1])
                if 'pause' in audio_txt:
                    self.tv.pause()
                elif 'play' in audio_txt:
                    self.tv.play()
        elif self.current_device == 'BROWSER':
            if 'you tube' in audio_txt or 'youtube' in audio_txt:
                print('opening youtube')
                for handle in browser.window_handles:
                    browser.switch_to.window(handle)
                    if browser.current_url == 'https://www.youtube.com/':
                        break
                if browser.current_url != 'https://www.youtube.com/':
                    browser.get('https://www.youtube.com/')

    def set_device(self, audio_txt):
        if 'tv' in audio_txt:
            self.current_device = 'TV'
        elif 'chrome' in audio_txt:
            self.current_device = 'BROWSER'


# options = webdriver.ChromeOptions()
# options.add_argument('user-data-dir=C:\\Users\\evila\\AppData\\Local\\Google\\Chrome\\User Data')
#
# browser = webdriver.Chrome(chrome_options=options)
netflix = sr.AudioFile('Netflix.wav')
controller = Controller()
with mic as source:
    print("Say Something")
    while True:
        r.adjust_for_ambient_noise(source, .25)
        audio = r.listen(source)

        try:
            controller.audio_command(r.recognize_sphinx(audio,
                                                        keyword_entries=[['disney', 1], ['tv', 1], ['netflix', 1],
                                                                         ['chrome', 1], ['youtube', 1], ['play', 1],
                                                                         ['pause', 1]]))
        except sr.UnknownValueError:
            print("Can't recognize command")
            pass
