import numpy as np
import cv2
import cv2.aruco as aruco
import os
import pickle
import time

# Check for camera calibration data
if not os.path.exists('calibration.pckl'):
    print("You need to calibrate the camera you'll be using. See calibration project directory for details.")
    exit()
else:
    f = open('calibration.pckl', 'rb')
    (cameraMatrix, distCoeffs, _, _) = pickle.load(f)
    f.close()
    if cameraMatrix is None or distCoeffs is None:
        print("Calibration issue. Remove calibration.pckl and recalibrate your camera with CalibrateCamera.py.")
        exit()

cap = cv2.VideoCapture(0)
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters =  cv2.aruco.DetectorParameters_create()

# Create grid board object we're using in our stream
board = aruco.GridBoard_create(
        markersX=2,
        markersY=2,
        markerLength=0.09,
        markerSeparation=0.01,
        dictionary=dictionary)

if cap.isOpened():
    #get video width and height and convert to int
    WIDTH = int (cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
    HEIGHT = int (cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #get FPS
    FPS = cap.get(cv2.CAP_PROP_FPS)

    print("Video w:", WIDTH, "h:", HEIGHT, "FPS:", FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('marker_output.mp4', fourcc, FPS, (WIDTH, HEIGHT))
else:
    print("ERROR! File ", vid, " isn't found!")

while(True):
    ret, frame = cap.read()
    if ret: 

        #make pic gray
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)

        # Refine detected markers
        # Eliminates markers not part of our board, adds missing markers to the board
        markerCorners, ids, rejectedImgPoints, recoveredIds = aruco.refineDetectedMarkers(
                image = frame,
                board = board,
                detectedCorners = markerCorners,
                detectedIds = markerIds,
                rejectedCorners = rejectedCandidates,
                cameraMatrix = cameraMatrix,
                distCoeffs = distCoeffs)

        if( markerCorners != [] ):
            #print(markerCorners)
            frame = cv2.aruco.drawDetectedMarkers(frame,
            markerCorners, markerIds)
            rvecs, tvecs, _ =  aruco.estimatePoseSingleMarkers(markerCorners, 1,
            cameraMatrix, distCoeffs)
            #print( rvecs, tvecs )
            for rvec, tvec in zip(rvecs, tvecs):
                frame = aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec, tvec, 1)

            retval, rvec, tvec =   aruco.estimatePoseBoard(markerCorners, markerIds, board, cameraMatrix, distCoeffs, rvec, tvec)
            dst, jacobian = cv2.Rodrigues(rvec)
            rvec_trs = dst.transpose()
            worldPos = - rvec_trs * tvec
            worldPos = [worldPos[0][0],worldPos[1][1], worldPos[2][2]]
            time.sleep(0.5)
            print( worldPos )

            cv2.imshow('frame',frame)
            out.write(frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
out.release()
cv2.destroyAllWindows()
