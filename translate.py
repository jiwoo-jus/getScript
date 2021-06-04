from googletrans import Translator
import codecs
import os

def trans(textFile, transFile):
    print(os.getcwd() + textFile)
    translator = Translator()
    with codecs.open(textFile, 'r', 'utf-8') as f:
        text = f.read()
    result = translator.translate(text, dest="ko")
    with open(transFile, 'w', encoding='utf-8') as f:
        f.write(result.text)
        print(result.text)
    print("done")