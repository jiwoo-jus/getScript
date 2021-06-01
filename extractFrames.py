import cv2


def capture(videoFile, imagePath, progressbar):
    roi = staticROI(videoFile)
    cap = cv2.VideoCapture(videoFile)
    count = 0
    progressbar.setMaximum(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while True:
        ret, image = cap.read()
        if not ret:
            break
        if (count % 30 == 0):
            clip = image[roi.y1:roi.y2, roi.x1:roi.x2].copy()
            cv2.imwrite(imagePath + "/target%d.jpg" % count, clip)
        count += 1
        progressbar.setValue(count)
    cap.release()


class staticROI(object):
    def __init__(self, videoFile):
        self.capture = cv2.VideoCapture(videoFile) #'C:\\Users\\parkj\\Desktop\\script1.mp4'
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