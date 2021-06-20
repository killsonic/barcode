# 웹캠으로 바코드 인식기

import cv2
import pyzbar.pyzbar as pyzbar
from playsound import playsound

data_list = []
used_codes = []


try:
    f = open('grbarcode_data.txt', 'r', encoding='utf8')
    data_list = f.readlines()
except FileNotFoundError:
    pass
else:
    f.close()
    

cap = cv2.VideoCapture(1)   #웹캠 장치 번호 0 or 1 or 2 장치 순서 찾아봐야 함

for i in data_list:
    used_codes.append(i.rsplit('\n'))

while True:
    success, frame = cap.read()

    if success:
        for code in pyzbar.decode(frame):
            my_code = code.data.decode('utf8')
            if my_code not in used_codes:
                print('인식 성공 : ', my_code)
                playsound('win_sound.wav')
                used_codes.append(my_code)

                #텍스트 파일에 저장
                f2 = open('grbarcode_data.txt', 'a', encoding='utf8')
                f2.write(my_code+'\n')
                f2.close()
                #바코드 캡쳐
                cv2.imwrite('./pic/' + my_code + '_img.png', frame)

            else:
                print('이미 인식된 코드')
                playsound('noop_sound.mp3')

        cv2.imshow('cam', frame)
        
        key = cv2.waitKey(1)
        if key == 27:   #ESC 키 누르면 종료
            break

cap.release()
cv2.destroyAllWindows()
