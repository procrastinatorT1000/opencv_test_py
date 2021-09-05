import numpy as np
import cv2


vid = "input.mp4"
cap = cv2.VideoCapture(vid)

while(True):
    ret, frame = cap.read()
    if ret: 

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(hsv, (0,50,50), (15,255,255))
        mask2 = cv2.inRange(hsv, (175,50,20), (180,255,255))
        mask = cv2.bitwise_or(mask1, mask2)
        #mask = mask1
        
        for i in zip(*np.where(mask == 255)):
            frame[i[0], i[1], 0] = 255
            frame[i[0], i[1], 1] = 255
            frame[i[0], i[1], 2] = 255
        cv2.imshow('frame',frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cv2.destroyAllWindows()
