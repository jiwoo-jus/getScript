import os, io, sys, cv2
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFileDialog, QLabel
from google.cloud import vision
from google.cloud.vision_v1 import types
from hanspell import spell_checker

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


class QtGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.num = 0
        self.setWindowTitle("Img to Text")  # 위젯타이틀 설정
        self.resize(300, 400)  # 사이즈 가로 300, 세로 400
        self.qclist = []
        self.position = 0
        self.Lgrid = QGridLayout()  # 격자모양표에 요소 순차 배치 레이아웃
        self.setLayout(self.Lgrid)
        self.label1 = QLabel('', self)  # 빈 문자열로 채운 라벨 생성
        self.label2 = QLabel('', self)
        self.label3 = QLabel('', self)
        self.label4 = QLabel('', self)
        addbutton1 = QPushButton('Open File', self)  # 'OpenFile' 문자열로 표시되는 버튼 생성
        self.Lgrid.addWidget(self.label1, 1, 1)  # (1,1)위치에 label1 부착
        self.Lgrid.addWidget(addbutton1, 2, 1)  # (2,1)위치에 addbutton1 부착
        addbutton1.clicked.connect(self.video_select)  # 사용자가 버튼 클릭시 add_open 함수 실행
        self.Lgrid.addWidget(self.label2, 3, 1)
        addbutton1.clicked.connect(self.video_cap)
        addbutton3 = QPushButton('Run', self)
        self.Lgrid.addWidget(self.label3, 4, 1)
        self.Lgrid.addWidget(addbutton3, 5, 1)
        addbutton3.clicked.connect(self.write_script)
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
        imagePath = savepath + '\\Capture'

        cap = cv2.VideoCapture(videoPath)
        count = 0

        while True:
            ret, image = cap.read()

            if not ret:
                break

            if (count % 30 == 0):
                ## 이미지 자르기 부분 수정 필요
                #clip = image[600:800, 300:-300].copy()
                cv2.imwrite(imagePath + "/target%d.jpg" % count, image)

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
        scriptPath = savepath + '\\Script'
        imagePath = savepath + '\\Capture'

        count = 0
        before = ''
        with open(scriptPath + '\\Script.txt', 'w', encoding='utf-8') as f:
            f.write('')

        while True:
            cap = cv2.VideoCapture(imagePath + '\\target' + str(count) + '.jpg')

            ret, image = cap.read()

            if (count % 30 == 0):
                if (count != 0):
                    with open(scriptPath + '\\NewTarget' + str(count - 30) + '.txt', 'r', encoding='utf-8') as f:
                        before = f.read()
                now = detect_text(imagePath + '\\target' + str(count) + '.jpg')
                with open(scriptPath + '\\NewTarget' + str(count) + '.txt', 'w', encoding='utf-8') as f:
                    f.write(now)
                if (before != now or before == ''):
                    with open(scriptPath + '\\Script.txt', 'a', encoding='utf-8') as f:
                        f.write(now)
                        print(now)
            count += 30
        self.label3.setText('Successed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QtGUI()
    app.exec_()