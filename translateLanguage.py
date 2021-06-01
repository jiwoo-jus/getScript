from googletrans import Translator
import codecs


def trans(textFile, transFile):
    print(textFile)
    translator = Translator()
    with codecs.open(textFile, 'r', 'utf-8') as f:
        text = f.read()
    result = translator.translate(text, dest="ko")
    with open(transFile, 'w', encoding='utf-8') as f:
        f.write(result.text)
    print(result.text)