import numpy as np
import cv2


vid = "input.mp4"
cap = cv2.VideoCapture(vid)

if cap.isOpened():
    #get video width and height and convert to int
    WIDTH = int (cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
    HEIGHT = int (cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #get FPS
    FPS = cap.get(cv2.CAP_PROP_FPS)

    print("Video w:", WIDTH, "h:", HEIGHT, "FPS:", FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, FPS, (WIDTH, HEIGHT))
else:
    print("ERROR! File ", vid, " isn't found!")

while(True):
    ret, frame = cap.read()
    if ret: 

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #Fill RED color mask in HSV format
        mask1 = cv2.inRange(hsv, (0,100,50), (15,255,255))
        mask2 = cv2.inRange(hsv, (175,100,20), (180,255,255))
        mask = cv2.bitwise_or(mask1, mask2)
        #mask = mask1
        
        for i in zip(*np.where(mask == 255)):
            frame[i[0], i[1], 0] = 255
            frame[i[0], i[1], 1] = 255
            frame[i[0], i[1], 2] = 255

        cv2.imshow('frame',frame)
        out.write(frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
out.release()
cv2.destroyAllWindows()
