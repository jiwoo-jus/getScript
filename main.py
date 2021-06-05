import os
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QFileDialog, QLabel, QProgressBar, QVBoxLayout, QHBoxLayout, QApplication
from PyQt5.QtCore import Qt
from extractFrames import capture
from writeScript import script
from textToSpeech import audio
from translate import trans


class QtGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("get script")
        self.resize(400, 100)

        self.layout = QVBoxLayout()

        self.topLayout = QVBoxLayout()
        self.mid1Layout = QHBoxLayout()
        self.mid2Layout = QVBoxLayout()
        self.bottomLayout = QGridLayout()
        self.bottom2Layout = QVBoxLayout()

        self.mid2Layout.addStretch(1)

        self.layout.addLayout(self.topLayout)
        self.layout.addLayout(self.mid1Layout)
        self.layout.addLayout(self.mid2Layout)
        self.layout.addLayout(self.bottomLayout)
        self.layout.addLayout(self.bottom2Layout)

        self.setLayout(self.layout)

        self.pbar1 = QProgressBar(self)
        self.pbar2 = QProgressBar(self)
        self.label1 = QLabel('', self)
        self.label2 = QLabel('', self)
        self.label4 = QLabel('Image Capture', self)
        self.label5 = QLabel('Create Script', self)
        self.addbutton1 = QPushButton('Open File', self)
        self.addbutton2 = QPushButton('Run', self)
        self.addbutton3 = QPushButton('TextToSpeech', self)
        self.addbutton4 = QPushButton('Translate', self)

        self.topLayout.addWidget(self.label1)
        self.topLayout.addWidget(self.addbutton1)
        self.mid1Layout.addWidget(self.label2)
        self.mid2Layout.addWidget(self.addbutton2)

        self.bottomLayout.addWidget(self.label4, 0, 0)
        self.bottomLayout.addWidget(self.label5, 1, 0)
        self.bottomLayout.addWidget(self.pbar1, 0, 1)
        self.bottomLayout.addWidget(self.pbar2, 1, 1)
        self.bottom2Layout.addWidget(self.addbutton3)
        self.bottom2Layout.addWidget(self.addbutton4)

        self.label2.setAlignment(Qt.AlignCenter)

        self.addbutton1.clicked.connect(self.video_select)
        self.addbutton2.clicked.connect(self.extract_frames)
        self.addbutton2.clicked.connect(self.write_script)
        self.addbutton3.clicked.connect(self.text_to_audio)
        self.addbutton4.clicked.connect(self.trans)
        self.show()

    def video_select(self):
        self.pbar1.setValue(0)
        self.pbar2.setValue(0)
        FileOpen = QFileDialog.getOpenFileName(self, 'Open file', 'sample')
        self.label1.setText(FileOpen[0])

    def extract_frames(self):
        self.label2.setText("Generate script...")
        print("\n>>> extract frames...")
        videoFile = self.label1.text().replace('/', '\\')
        savepath = videoFile.split('\\')[:-1]
        savepath = ('\\').join(savepath)
        os.chdir(savepath)
        if not os.path.exists('Capture'):
            os.makedirs('Capture')
        imagePath = savepath + '\\Capture'
        capture(videoFile, imagePath, self.pbar1)

    def write_script(self):
        print("\n>>> write script...")
        savepath = self.label1.text().split('/')
        videoname = savepath.pop().split('.')[0]
        savepath = ('\\').join(savepath)
        os.chdir(savepath)
        imagePath = savepath + '\\Capture'
        scriptFile = savepath + '\\' + videoname + '_script.txt'
        script(imagePath, savepath, scriptFile, self.pbar2)

    def text_to_audio(self):
        print("\n>>> convert to audio...")
        savepath = self.label1.text().split('/')
        videoname = savepath.pop().split('.')[0]
        scriptname = videoname + '_script.txt'
        savepath = ('\\').join(savepath)
        os.chdir(savepath)
        audioFile = savepath + '\\' + videoname + '_script.mp3'
        audio(audioFile, scriptname)

    def trans(self):
        print("\n>>> translate...")
        savepath = self.label1.text().split('/')
        videoname = savepath.pop().split('.')[0]
        scriptname = videoname + '_script.txt'
        transname = videoname + '_translated_script.txt'
        savepath = ('\\').join(savepath)
        os.chdir(savepath)
        trans(scriptname, transname)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QtGUI()
    app.exec_()