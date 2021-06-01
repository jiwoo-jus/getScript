import os
from PyQt5.QtWidgets import QGridLayout, QFileDialog, QLabel
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar
from writeScript import script
from extractFrames import capture


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
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(15, 330, 300, 25)
        self.pbar2 = QProgressBar(self)
        self.pbar2.setGeometry(15, 150, 300, 25)

        self.label1 = QLabel('', self)
        self.label2 = QLabel('', self)
        self.label3 = QLabel('', self)

        addbutton1 = QPushButton('Open File', self)
        self.Lgrid.addWidget(self.label1, 1, 1)
        self.Lgrid.addWidget(addbutton1, 2, 1)
        addbutton1.clicked.connect(self.video_select)

        addbutton2 = QPushButton('Run', self)
        self.Lgrid.addWidget(self.label2, 3, 1)
        addbutton2.clicked.connect(self.extract_frames)

        self.Lgrid.addWidget(self.label3, 4, 1)
        self.Lgrid.addWidget(addbutton2, 5, 1)
        addbutton2.clicked.connect(self.write_script)
        self.show()

    def video_select(self):
        FileOpen = QFileDialog.getOpenFileName(self, 'Open file', r'C:\Users\parkj\Downloads')
        self.label1.setText(FileOpen[0])

    def extract_frames(self):
        self.label2.setText("Doing extract_frames")
        print("\nextract frames...")
        videoFile = self.label1.text()
        print(videoFile)
        savepath = videoFile.split('/')[:-1]
        savepath = ('\\').join(savepath)
        os.chdir(savepath)
        if not os.path.exists('Capture'):
            os.makedirs('Capture')
        imagePath = savepath + '\\Capture'
        capture(videoFile, imagePath, self.pbar2)
        self.label2.setText("Successed extract_frames!")

    def write_script(self):
        self.label3.setText('Doing write_script')
        print("\nwrite script...")
        savepath = self.label1.text().split('/')
        filename = savepath.pop().split('.')[0]
        savepath = ('\\').join(savepath)
        os.chdir(savepath)
        imagePath = savepath + '\\Capture'
        script(imagePath, savepath, filename, self.pbar)
        self.label3.setText('Successed Write_script!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QtGUI()
    app.exec_()