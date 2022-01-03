# 모듈 불러오기: import 모듈 이름 - 이미지 사용을 위한 opencv,
# 이미지 저장 파일명 사용을 위한 datetime

import cv2
import datetime

video_capture = cv2.VideoCapture(1)
def capture(self):
    while (True):
        grabbed, frame = video_capture.read()
        cv2.imshow('Original Video', frame)

        key = cv2.waitKey(1);
        if key == ord('q'):
            break
        elif key == ord('s'):
            file = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f") + '.jpg'
            cv2.imwrite(file, frame)
            print(file, 'saved')
            return file

    video_capture.release()
    cv2.destroyWindow('original Video')