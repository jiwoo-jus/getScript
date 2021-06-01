import os, io, sys, cv2, shutil
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFileDialog, QLabel
from google.cloud import vision
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar
from PyQt5.QtCore import QBasicTimer
from extractFrames import staticROI

os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r"C:\WorkSpace\pycharm\pythonProject-jiwjus_img2txt\jw-img2txt-8f65dde3d9fb.json"


def detect_text(path):
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    string = ''
    for text in texts[:1]:
        string = text.description
    ret = string.split()
    return string


def similarity(before, now):
    before = before.replace(' ', '')
    now = now.replace(' ', '')
    same_list = []
    for i in now:
        if i in before:
            same_list.append(i)
    similarity = (len(same_list) * 2 + 1) / ((len(before) + len(now)) + 1)
    return similarity


def script(imagePath, savePath, videoname, progressbar):
    imglen = len(os.listdir(imagePath))
    count = 0
    before = ''
    scriptFile = savePath + '\\' + videoname + '_script.txt'
    with open(scriptFile, 'w', encoding='utf-8') as f:
        f.write('')
    with open(savePath + '\\target.txt', 'w', encoding='utf-8') as f:
        f.write('')

    progressbar.setMaximum(imglen)

    while (count < imglen):
        with open(savePath + '\\target.txt', 'r', encoding='utf-8') as f:
            before = f.read()
        now = detect_text(imagePath + '\\target' + str(count * 30) + '.jpg')
        if (len(now) == 0):
            pass
        if (similarity(before, now) < 0.7):
            with open(scriptFile, 'a', encoding='utf-8') as f:
                f.write(now)
                print(now)
        with open(savePath + '\\target.txt', 'w', encoding='utf-8') as f:
            f.write(now)
        count += 1
        progressbar.setValue(count)

    os.remove(savePath + '\\target.txt')
    shutil.rmtree(imagePath)