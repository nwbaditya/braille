import cv2
import numpy as np
from imutils.perspective import four_point_transform


cap = cv2.VideoCapture(2)

WIDTH, HEIGHT = 800, 600
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

kernel_erode = np.ones((5, 5), np.uint8)

kernel_sharp = np.array([[0, -1, 0],
                        [-1, 5,-1],
                        [0, -1, 0]])

def scan_detection(image):
    global document_contour

    document_contour = np.array([[0, 0], [WIDTH, 0], [WIDTH, HEIGHT], [0, HEIGHT]])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, threshold = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
    # threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 53 , 5)

    threshold = cv2.erode(threshold, kernel_erode)
    cv2.imshow("process", threshold)

    contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.015 * peri, True)
            if area > max_area and len(approx) == 4:
                document_contour = approx
                max_area = area

    cv2.drawContours(frame, [document_contour], -1, (0, 255, 0), 3)


while(True):
    # ret, frame = cap.read()
    frame = cv2.imread('test3.jpg')
    # if not ret:
        # break

    key = cv2.waitKey(1)

    if key & 0xFF == 27:
        break
    elif key & 0xFF == 32:
        print('Space Pressed')
        img = warped
        cv2.imwrite('test.png', img)
        img_copy = img.copy()
        break
    else:   
        frame_copy = frame.copy()
        scan_detection(frame_copy)
        cv2.imshow("input", cv2.resize(frame, (WIDTH,HEIGHT)))
        warped = four_point_transform(frame_copy, document_contour.reshape(4, 2))
        warped = cv2.resize(warped, (600, 600))
        cv2.imshow("Warped", warped)

cap.release()
cv2.destroyAllWindows()

cv2.imshow('Captured Image', img)
cv2.waitKey(0)