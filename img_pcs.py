import cv2
import numpy as np

def nothing(x):
    pass
col = 48
row = 25

# cv2.namedWindow('Thresh')

# cv2.createTrackbar('min', 'Thresh', 5, 255, nothing)
# cv2.createTrackbar('max', 'Thresh', 0, 255, nothing)


kernel_sharp = np.array([[0, -1, 0],
                        [-1, 5,-1],
                        [0, -1, 0]])

kernel_erode = np.ones((3,3), np.uint8)

img = cv2.imread('test.png')
img_copy = img.copy()
# cv2.imshow('orig', img)

while(True):
    hnow = 0
    wnow = 0
    img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    img_cropped = img_gray[10:(600-10), 25 : (600-25)]
    img_cropped = cv2.resize(img_cropped, (600,600))

    img_blur = cv2.GaussianBlur(img_cropped, (3,3), 0)
    # cv2.imshow('blur', img_blur)

    img_sharp = cv2.filter2D(img_cropped, ddepth=-1, kernel=kernel_sharp)
    # img_sharp = cv2.filter2D(img_sharp, ddepth=-1, kernel=kernel_sharp)
    # cv2.imshow('sharpen', img_sharp)


    # min = cv2.getTrackbarPos('min', 'Thresh')
    # max = cv2.getTrackbarPos('max', 'Thresh')

    img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 121 , 5)
    # img_erode = cv2.erode(img_thresh, kernel_erode, iterations= 1 )
    # img_erode = cv2.dilate(img_erode, kernel_erode, iterations= 1 )
    contours, _ = cv2.findContours(img_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # for c in range (0, col):
    #     for r in range(0, row):
    #         cv2.line(img_cropped, (10 + wnow, 32 + hnow), (580 - wnow,32 + hnow), (255,0,0), 1)

    #         # cv2.imshow('cropped', img_cropped)
    #         hnow = hnow + 20
    #     cv2.line(img_cropped, (10 + wnow, 32 + 480), (10 + wnow,32 + 0), (255,0,0), 1)
    #     wnow = wnow + 12
    cv2.imshow('cropped', img_cropped)


    # cv2.line(img_cropped, (10 , 32), (10,592), (255,0,0), 1)
    # cv2.line(img_cropped, (10,32), (580,32), (255,0,0), 1)
    # cv2.line(img_cropped, (10,54), (580,54), (255,0,0), 1)

    # cv2.drawContours(img_cropped, contours, -1, (0, 255, 0), 1)

    # cv2.imshow('cropped', img_cropped)
    # cv2.imshow('img', img_cropped)
    cv2.imshow('thres', img_thresh)

    key = cv2.waitKey(1)
    if key & 0xff == 27:
        break

cv2.destroyAllWindows()