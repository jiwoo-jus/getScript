# import codecs
import cv2
import os, io, sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFileDialog, QLabel
from google.cloud import vision
from hanspell import spell_checker

os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r"C:\WorkSpace\pycharm\pythonProject-jiwjus_img2txt\jw-img2txt-8f65dde3d9fb.json"

class QtGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.num = 0
        self.setWindowTitle("Img to Text") # 위젯타이틀 설정
        self.resize(300, 400) # 사이즈 가로 300, 세로 400
        self.qclist = []
        self.position = 0
        self.Lgrid = QGridLayout() # 격자모양표에 요소 순차 배치 레이아웃
        self.setLayout(self.Lgrid)
        self.label1 = QLabel('', self) # 빈 문자열로 채운 라벨 생성
        self.label2 = QLabel('', self)
        self.label3 = QLabel('', self)
        self.label4 = QLabel('', self)
        addbutton1 = QPushButton('Open File', self) # 'OpenFile' 문자열로 표시되는 버튼 생성
        self.Lgrid.addWidget(self.label1, 1, 1) # (1,1)위치에 label1 부착
        self.Lgrid.addWidget(addbutton1, 2, 1) # (2,1)위치에 addbutton1 부착
        addbutton1.clicked.connect(self.add_open) # 사용자가 버튼 클릭시 add_open 함수 실행
        addbutton2 = QPushButton('Save File', self)
        self.Lgrid.addWidget(self.label2, 3, 1)
        self.Lgrid.addWidget(addbutton2, 4, 1)
        addbutton2.clicked.connect(self.add_save)
        addbutton3 = QPushButton('Run', self)
        self.Lgrid.addWidget(self.label3, 5, 1)
        self.Lgrid.addWidget(addbutton3, 6, 1)
        addbutton3.clicked.connect(self.detect_text)
        addbutton4 = QPushButton('Run *remove newline', self)
        self.Lgrid.addWidget(self.label4, 7, 1)
        self.Lgrid.addWidget(addbutton4, 8, 1)
        addbutton4.clicked.connect(self.removeNewLine)
        self.show()


    def add_open(self):
        FileOpen = QFileDialog.getOpenFileName(self, 'Open file', r'C:\Users\parkj\Downloads')

        self.label1.setText(FileOpen[0])

    def add_save(self):
        savepath = self.label1.text().split('/')
        filename = (savepath.pop()).split('.')[0].capitalize()
        savepath = ('\\').join(savepath)
        os.chdir(savepath)
        os.mkdir('Capture')
        videoPath = self.label1.text()
        imagePath = savepath + '\\Capture'

        cap = cv2.VideoCapture(videoPath)
        count = 0

        while True:
            ret, image = cap.read()

            if not ret:
                break
            if (count % 30 == 0):
                clip = image[800:950, 450:1500].copy()
                cv2.imwrite(imagePath + "/target%d.jpg" % count, clip)

            print('%d.jpg done' % count)
            count += 1

        cap.release()

        self.label2.setText(imagePath) # 선택 경로를 label2에 부착


    def detect_text(self):
        client = vision.ImageAnnotatorClient() # 코드 앞부분에 클라우드 콘솔 서비스 계정 키파일 경로 명시해둠
        path = self.label1.text() # 파일 오픈 위치

        # 로컬 이미지 파일(바이너리 데이터)을 비전에 전달하기 위해서 base64라는 인코딩을 거쳐 문자열로 변환해 전송
        with io.open(path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

        response = client.text_detection(image=image) # response에는 이미지에서 문자 감지한 것에 대한 각종 정보가 다 들어있음
        texts = response.text_annotations # 여기서 필요한 것

        text = format(texts[0].description) # 인덱스 0 위치에 전체 통 문자열이 담겨있음.

        with open(self.label2.text(), 'w', encoding='utf-8') as f: # 지정한 저장 경로에 파일 작성
            f.write(text)

        self.label3.setText('Successed')

    def removeNewLine(self):
        client = vision.ImageAnnotatorClient()
        path = self.label1.text()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations

        text = format(texts[0].description).split("\n")

        for i in range(len(text) - 1):
            l1 = text[i].split()[-1] if (len(text[i]) >= 2) else ""
            l2 = text[i + 1].split()[0] if (len(text[i + 1]) >= 2) else ""
            str = l1 + l2  # i번째줄 문장의 끝 단어와 i+1번째줄 문장의 첫 단어를 일단 붙인다
            # print(spell_checker.check(str).errors, spell_checker.check(str).original, spell_checker.check(str).checked)
            if (spell_checker.check(str).errors > 0):  # 맞춤법검사해서 에러 있으면 i번째 문장 끝에 띄어쓰기(공백) 붙여서 새 텍스트파일에 삽입
                with open(self.label2.text(), 'a', encoding='utf-8') as f:
                    f.write(text[i] + " ")
                # print("fiexd newline : ", b[i] + " ")
            else:  # 맞춤법검사해서 에러 없으면 i번째 문장 그대로 새 텍스트파일에 삽입
                with open(self.label2.text(), 'a', encoding='utf-8') as f:
                    f.write(text[i])

        self.label4.setText('Successed')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QtGUI()
    app.exec_()

