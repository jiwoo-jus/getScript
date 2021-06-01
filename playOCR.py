import os, io, sys, cv2, shutil
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFileDialog, QLabel
from google.cloud import vision
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar
from PyQt5.QtCore import QBasicTimer
from setROI import staticROI

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


def script(imagePath, scriptPath):
    imglen = len(os.listdir(imagePath))
    count = 0
    before = ''
    with open(scriptPath + '\\Script.txt', 'w', encoding='utf-8') as f:
        f.write('')
    with open(scriptPath + '\\target.txt', 'w', encoding='utf-8') as f:
        f.write('')
    while (count < imglen * 30):
        with open(scriptPath + '\\target.txt', 'r', encoding='utf-8') as f:
            before = f.read()
        now = detect_text(imagePath + '\\target' + str(count) + '.jpg')
        if (len(now) == 0):
            pass
        if (similarity(before, now) < 0.7):
            with open(scriptPath + '\\Script.txt', 'a', encoding='utf-8') as f:
                f.write(now)
                print(now)
        with open(scriptPath + '\\target.txt', 'w', encoding='utf-8') as f:
            f.write(now)
        count += 30
    os.remove(scriptPath + '\\target.txt')
    shutil.rmtree(imagePath)