import os, io, sys, cv2, shutil
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFileDialog, QLabel
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r"C:\WorkSpace\pycharm\pythonProject-jiwjus_img2txt\jw-img2txt-8f65dde3d9fb.json"

class staticROI(object):
    def __init__(self, videoRef):
        print(videoRef)
        self.capture = cv2.VideoCapture(videoRef) #'C:\\Users\\parkj\\Desktop\\script1.mp4'
        # Bounding box reference points and boolean if we are extracting coordinates
        self.image_coordinates = []
        self.extract = False
        self.selected_ROI = False
        self.update()

    def update(self):
        while True:
            if self.capture.isOpened():
                # Read frame
                (self.status, self.frame) = self.capture.read()
                cv2.imshow('image', self.frame)
                key = cv2.waitKey(2)
                # Crop image
                if key == ord('c'):
                    self.clone = self.frame.copy()
                    cv2.namedWindow('image')
                    cv2.setMouseCallback('image', self.extract_coordinates)
                    while True:
                        key = cv2.waitKey(2)
                        cv2.imshow('image', self.clone)
                        # Crop and display cropped image
                        if key == ord('c'):
                            self.crop_ROI()
                        # Resume video
                        if key == ord('r'):
                            break
                        if key == ord('q'):
                            cv2.destroyAllWindows()
                            return
                # Close program with keyboard 'q'
                if key == ord('q'):
                    cv2.destroyAllWindows()
                    exit(1)
            else:
                pass

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x,y)]
            self.extract = True
        # Record ending (x,y) coordintes on left mouse bottom release
        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x,y))
            self.extract = False
            self.selected_ROI = True
            # Draw rectangle around ROI
            cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (0,255,0), 2)
        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.frame.copy()
            self.selected_ROI = False

    def crop_ROI(self):
        if self.selected_ROI:
            self.cropped_image = self.frame.copy()
            self.x1 = self.image_coordinates[0][0]
            self.y1 = self.image_coordinates[0][1]
            self.x2 = self.image_coordinates[1][0]
            self.y2 = self.image_coordinates[1][1]
            self.cropped_image = self.cropped_image[self.y1:self.y2, self.x1:self.x2]
            print('Cropped image: {} {}'.format(self.image_coordinates[0], self.image_coordinates[1]))
            #return x1, y1, x2, y2
        else:
            print('Select ROI to crop before cropping')


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
    before_list = before.replace(' ', '')
    now_list = now.replace(' ', '')
    same_list = []
    for i in now_list:
        if i in before_list:
            same_list.append(i)
    similarilty = len(same_list) * 2 / (len(before_list) + len(now_list))
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
        videoPath = self.label1.text()
        roi = staticROI(videoPath)
        print(roi.y1, roi.y2, roi.x1, roi.x2)
        savepath = self.label1.text().split('/')
        filename = (savepath.pop()).split('.')[0].capitalize()
        savepath = ('\\').join(savepath)
        os.chdir(savepath)
        if not os.path.exists('Capture'):
            os.makedirs('Capture')
        imagePath = savepath + '\\Capture'

        cap = cv2.VideoCapture(videoPath)
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
        imglen = len(os.listdir(imagePath))

        count = 0
        before = ''
        with open(scriptPath + '\\Script.txt', 'w', encoding='utf-8') as f:
            f.write('')

        while (count < imglen * 30):
            cap = cv2.VideoCapture(imagePath + '\\target' + str(count) + '.jpg')
            ret, image = cap.read()

            if (count % 30 == 0):
                if (count != 0):
                    with open(scriptPath + '\\target.txt', 'r', encoding='utf-8') as f:
                        before = f.read()
                now = detect_text(imagePath + '\\target' + str(count) + '.jpg')
                if (similarilty(before, now) < 0.7 or before == ''):
                    with open(scriptPath + '\\Script.txt', 'a', encoding='utf-8') as f:
                        f.write(now)
                        print(now)
                with open(scriptPath + '\\target.txt', 'w', encoding='utf-8') as f:
                    f.write(now)
            count += 30
        cap.release()
        os.remove(scriptPath + '\\target.txt')
        shutil.rmtree(imagePath)
        self.label3.setText('Successed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QtGUI()
    app.exec_()