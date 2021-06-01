import os, io, sys, cv2, shutil
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFileDialog, QLabel
from google.cloud import vision
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar
from PyQt5.QtCore import QBasicTimer
from playOCR import detect_text, script
from setROI import staticROI


def capture(videoFile, imagePath):
    roi = staticROI(videoFile)
    cap = cv2.VideoCapture(videoFile)
    count = 0
    while True:
        ret, image = cap.read()
        if not ret:
            break
        if (count % 30 == 0):
            clip = image[roi.y1:roi.y2, roi.x1:roi.x2].copy()
            cv2.imwrite(imagePath + "/target%d.jpg" % count, clip)
        count += 1
    cap.release()


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
        self.label2.setText("Doing video_cap")
        videoFile = self.label1.text()
        savepath = videoFile.split('/')[:-1]
        savepath = ('\\').join(savepath)
        os.chdir(savepath)
        if not os.path.exists('Capture'):
            os.makedirs('Capture')
        imagePath = savepath + '\\Capture'
        capture(videoFile, imagePath)
        self.label2.setText("Successed Video_cap!")

    def write_script(self):
        self.label3.setText('Doing write_script')
        savepath = self.label1.text().split('/')[:-1]
        savepath = ('\\').join(savepath)
        os.chdir(savepath)
        if not os.path.exists('Script'):
            os.makedirs('Script')
        imagePath = savepath + '\\Capture'
        scriptPath = savepath + '\\Script'
        script(imagePath, scriptPath)
        self.label3.setText('Successed write_script!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QtGUI()
    app.exec_()