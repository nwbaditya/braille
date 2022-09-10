import cv2
import numpy as np

cap = cv2.VideoCapture(0)

WIDTH, HEIGHT = 1280, 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

output_width, output_height = 250, 350


circles = np.zeros((4,2), np.int)
counter = 0


def mouse_handler(event, x, y, flags, params):
    global counter

    if event == cv2.EVENT_LBUTTONDOWN:
        # print(x,y)
        circles[counter] = x,y
        counter = counter + 1
        print(circles)

        if counter > 4:
            counter = 0

while(1):
    ret, frame = cap.read()
    if not ret:
        break
    
    if counter == 4:
        pts1 = np.float32([circles[0], circles[1], circles[2], circles[3]])
        pts2 = np.float32([[0,0], [output_width, 0], [0, output_height], [output_width, output_height]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        frame_output = cv2.warpPerspective(frame, matrix, (output_width, output_height))
        # cv2.imshow("Output", frame_output)
        current_x = 0
        current_y = 0

        for i in range (0, 10):
            for j in range(0, 10):
                window_area = frame_output[current_y:(current_y+35), current_x:(current_x+25)]
                print(current_x, current_y)
                cv2.rectangle(frame_output, (current_x, current_y),(current_x+25, current_y+35), (0,255,0), 1)
                cv2.imshow("window_area", window_area)
                cv2.imshow("Output", frame_output)
                current_x = current_x + 25
                cv2.waitKey(100)
            current_x = 0
            current_y = current_y + 35
        break

    for x in range (0,4):
        cv2.circle(frame, (circles[x][0], circles[x][1]), 3, (0, 255, 0), cv2.FILLED)

    cv2.imshow("Input", frame)
    cv2.setMouseCallback("Input", mouse_handler)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
