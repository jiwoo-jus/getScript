import os, codecs
from gtts import gTTS


def audio(audioFile, videoname):
        print(audioFile)
        scriptFile = videoname + '_script.txt'
        with codecs.open(scriptFile, 'r', 'utf-8') as f:
                script = f.read()
        tts = gTTS(text=script, lang='ko')  # 영어는 lang='en'
        if os.path.isfile(audioFile):
                os.remove(audioFile)
        tts.save(audioFile)