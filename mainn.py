import cv2
import numpy as np

def nothing(x):
    pass
col = 48
row = 25

# cv2.namedWindow('Thresh')

# cv2.createTrackbar('min', 'Thresh', 5, 255, nothing)
# cv2.createTrackbar('max', 'Thresh', 0, 255, nothing)
translator = {
    "000000":" ",
    "100000":"a",
    "101000":"b",
    "110000":"c",
    "110100":"d",
    "100100":"e",
    "111000":"f",
    "111100":"g",
    "101100":"h",
    "011000":"i",
    "011100":"j",
    "100010":"k",
    "101010":"l",
    "110010":"m",
    "110110":"n",
    "100110":"o",
    "111010":"p",
    "111110":"q",
    "101110":"r",
    "011010":"s",
    "011110":"t",
    "100011":"u",
    "101011":"v",
    "011101":"w",
    "110011":"x",
    "110111":"y",
    "100111":"z",
    "010111":"#"
}

kernel_sharp = np.array([[0, -1, 0],
                        [-1, 5,-1],
                        [0, -1, 0]])

kernel_erode = np.ones((3,3), np.uint8)

img = cv2.imread('test.png')
img_copy = img.copy()
# cv2.imshow('orig', img)

filteredContours = []
coordinatePoint = []

approx_space_x = 10
approx_space_y = 10

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

    for contour in contours:
        contour_area = cv2.contourArea(contour)
        if contour_area > 5 and contour_area < 15:
            filteredContours.append(contour)

    coordinates = []
    for c in filteredContours:
        M = cv2.moments(c)
        cx = int(M["m10"]/M["m00"])
        cy = int(M["m01"]/M["m00"])
        coordinates.append((cx,cy))

        cv2.circle(img_cropped, (cx, cy), 3, (0,255,0), -1)

    # print(filteredContours[0][1])
    # cv2.drawContours(img_cropped, filteredContours, -1, (0,255,0), 1)

    coordinates_flagged = list(map(lambda x : [x,False], coordinates))
    # finding columns and rows

    columns = []
    rows = []

    # find columns
    for coord_idx in range(len(coordinates_flagged)):
        coord, flagged = coordinates_flagged[coord_idx]

        if not flagged:
            #print(coordinates_flagged[coord_idx])
            coordinates_flagged[coord_idx][1] = True
            avg_x = coord[0]
            checked_counter = 0

            for coord_idx_compare in range(coord_idx+1, len(coordinates_flagged)):
                coord_comp, flagged_comp = coordinates_flagged[coord_idx_compare]
                if not flagged_comp:
                    if abs(avg_x-coord_comp[0]) < approx_space_x:
                        checked_counter+=1
                        delta_x = coord_comp[0] - avg_x
                        avg_x += delta_x/checked_counter
                        coordinates_flagged[coord_idx_compare][1] = True
                        

            columns.append(avg_x)
        
    # find rows
    coordinates_flagged = list(map(lambda x : [x,False], coordinates))

    for coord_idx in range(len(coordinates_flagged)):
        coord, flagged = coordinates_flagged[coord_idx]

        if not flagged:
            coordinates_flagged[coord_idx][1] = True
            avg_y = coord[1]
            checked_counter = 0

            for coord_idx_compare in range(coord_idx+1, len(coordinates_flagged)):
                coord_comp, flagged_comp = coordinates_flagged[coord_idx_compare]
                if not flagged_comp:
                    if abs(avg_y-coord_comp[1]) < approx_space_x:
                        checked_counter+=1
                        delta_y = coord_comp[1] - avg_y
                        avg_y += delta_x/checked_counter
                        coordinates_flagged[coord_idx_compare][1] = True
                        

            rows.append(avg_y)
    
    columns = sorted(columns)
    rows = sorted(rows)


    img_cropped_withlines = img_cropped.copy()

    for x in columns:
        x = int(x)
        cv2.line(img_cropped_withlines,(x,0),(x,600),(0,0,0),1)

    for y in rows:
        y = int(y)
        cv2.line(img_cropped_withlines,(0,y),(600,y),(0,0,0),1)

    # translation
    # segment every 3 rows and 2 columns

    codes = []
    print("rc:",len(rows),len(columns))
    for i in range(0,len(rows),3):
        for j in range(0,len(columns),2):
            code = [0,0,0,0,0,0]
            code[0] = int(img_thresh[int(rows[i])][int(columns[j])] == 255)
            code[1] = int(img_thresh[int(rows[i])][int(columns[j])+1] == 255)
            code[2] = int(img_thresh[int(rows[i])+1][int(columns[j])] == 255)
            code[3] = int(img_thresh[int(rows[i])+1][int(columns[j])+1] == 255)
            code[4] = int(img_thresh[int(rows[i])+2][int(columns[j])] == 255)
            code[5] = int(img_thresh[int(rows[i])+2][int(columns[j])+1] == 255)


            codes.append(''.join(list(map(lambda x : str(x), code))))
    #print(codes)
    def convert(c):
        if c in translator.keys():
            return translator[c]
        return "_"
    translated = list(map(convert,codes))

    print(''.join(translated))
        
    
    

        

    
        

    


    cv2.imshow('cropped', img_cropped)
    cv2.imshow('cropped_withlines', img_cropped_withlines)


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