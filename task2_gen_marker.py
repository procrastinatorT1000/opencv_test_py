import cv2
import numpy as np
# Загрузить предопределенный словарь
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
# Сгенерировать маркер
W_SIZE = 400
H_SIZE = 400

markerImage = np.zeros((W_SIZE, H_SIZE), dtype=np.uint8)
markerImage = cv2.aruco.drawMarker(dictionary, 33, 400, markerImage, 1);

outIm = cv2.copyMakeBorder(markerImage, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=[255,255,255])

cv2.imwrite('marker33_1.png',outIm)

