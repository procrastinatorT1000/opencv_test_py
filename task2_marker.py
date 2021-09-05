import numpy as np
import cv2

cap = cv2.VideoCapture(0)
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters =  cv2.aruco.DetectorParameters_create()

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

        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)

        if( markerCorners != [] ):
            print(markerCorners)
            frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)

        #cv2.aruco.drawAxis(frame, 

        cv2.imshow('frame',frame)
        out.write(frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
out.release()
cv2.destroyAllWindows()
