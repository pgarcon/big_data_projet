# Import
from gtts import gTTS
from IPython.display import Audio
import os

# The text that you want to convert to audio
mytext = ''
language = 'fr'
f = open("tts/tts.txt", encoding="utf-8")

for line in f.readlines():
    if line != "\n":
        if "<new>" in line:
            gTTS(text=mytext, lang=language, slow=False).save("tts/audio.mp3")
            mytext = ''
        else:
            mytext += line

gTTS(text=mytext, lang=language, slow=False).save("tts/audio.mp3")
f.close()

Audio("tts/audio.mp3", autoplay=True)
