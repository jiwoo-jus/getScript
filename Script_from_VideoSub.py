#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os, io, sys,cv2, shutil
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFileDialog, QLabel
from google.cloud import vision
from google.cloud.vision_v1 import types
from hanspell import spell_checker

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

def similarilty(before, now):
    before_list = before.replace(' ','')
    now_list = now.replace(' ','')
    same_list = []
    for i in now_list:
        if i in before_list:
            same_list.append(i)
    similarilty = len(same_list)*2/ (len(before_list)+len(now_list))
    return similarilty


class QtGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.num = 0
        self.setWindowTitle("Img to Text")
        self.resize(300, 400)
        self.qclist = []
        self.position = 0
        self.Lgrid = QGridLayout()
        self.setLayout(self.Lgrid)
        
        self.label1 = QLabel('', self)
        self.label2 = QLabel('', self)
        self.label3 = QLabel('', self)
        
        addbutton1 = QPushButton('Open File', self)
        self.Lgrid.addWidget(self.label1, 1, 1)
        self.Lgrid.addWidget(addbutton1, 2, 1)
        addbutton1.clicked.connect(self.video_select)
        
        addbutton2 = QPushButton('Run', self)
        self.Lgrid.addWidget(self.label2, 3, 1)
        addbutton2.clicked.connect(self.video_cap)
        
        self.Lgrid.addWidget(self.label3, 4, 1)
        self.Lgrid.addWidget(addbutton2, 5, 1)
        addbutton2.clicked.connect(self.write_script)
        self.show()

    def video_select(self):
        FileOpen = QFileDialog.getOpenFileName(self, 'Open file', r'C:\Users\parkj\Downloads')

        self.label1.setText(FileOpen[0])
        
    def video_cap(self):
        savepath = self.label1.text().split('/')
        filename = (savepath.pop()).split('.')[0].capitalize()
        savepath = ('\\').join(savepath)
        os.chdir(savepath)
        if not os.path.exists('Capture'):
            os.makedirs('Capture')
        videoPath = self.label1.text()
        imagePath = savepath+'\\Capture'

        cap = cv2.VideoCapture(videoPath)
        count = 0

        while True:
            ret, image = cap.read()

            if not ret:
                break

            if(count % 30 == 0):
                ## 이미지 자르기 부분 수정 필요
                clip = image[600:800, 300:-300].copy()
                cv2.imwrite(imagePath + "/target%d.jpg" % count, clip)
                
            count += 1

        cap.release()
        self.label2.setText("Done!")
        
    def write_script(self):
        savepath = self.label1.text().split('/') 
        filename = (savepath.pop()).split('.')[0].capitalize()
        savepath = ('\\').join(savepath)
        os.chdir(savepath)
        if not os.path.exists('Script'):
            os.makedirs('Script')
        scriptPath = savepath+'\\Script'
        imagePath = savepath+'\\Capture'
        imglen = len(os.listdir(imagePath))
        
        count = 0
        before=''
        with open(scriptPath+'\\Script.txt', 'w', encoding='utf-8') as f:
                f.write('')
                
        while (count < imglen*30):
            cap = cv2.VideoCapture(imagePath + '\\target'+str(count)+'.jpg')
            ret, image = cap.read()

            if(count % 30 == 0):
                if (count != 0):
                    with open(scriptPath+'\\target.txt', 'r', encoding='utf-8') as f:
                        before = f.read()
                now = detect_text(imagePath + '\\target'+str(count)+'.jpg')
                if (similarilty(before, now) < 0.7 or before==''):
                    with open(scriptPath+'\\Script.txt', 'a', encoding='utf-8') as f:
                        f.write(now)
                        print(now)
                with open(scriptPath+'\\target.txt', 'w', encoding='utf-8') as f:
                    f.write(now)
            count += 30
        cap.release()
        os.remove(scriptPath+'\\target.txt')
        shutil.rmtree(imagePath)
        self.label3.setText('Successed')   

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QtGUI()
    app.exec_()

