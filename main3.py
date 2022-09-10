import cv2
import numpy as np

cap = cv2.VideoCapture(2)

WIDTH, HEIGHT = 1280, 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)


def mapp(h):
    h = h.reshape((4,2))
    hnew = np.zeros((4,2),dtype = np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h,axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew

while(True):
    ret, frame = cap.read()
    frame_copy = frame.copy()
    gray_frame = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2GRAY)
    blur_frame = cv2.GaussianBlur(gray_frame, (5,5),0)
    cv2.imshow("Blur", blur_frame)
    edges_frame = cv2.Canny(blur_frame, 50, 100)
    cv2.imshow("Edges", edges_frame)

    contours, hierarchy = cv2.findContours(edges_frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse=True)

    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, peri*0.02, True)

        if len(approx) == 4:
            target = approx
            
    cv2.drawContours(frame_copy, target, -1, (0,255,0), 3)
    cv2.imshow('Contours', frame_copy)
    approx = mapp(target)
    pts = np.float32([[0,0], [800,0],[800,800],[0,800]])
    output = cv2.getPerspectiveTransform(approx, pts)
    dst = cv2.warpPerspective(frame_copy, output, (800,800))

    cv2.imshow('Scanned', dst)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()