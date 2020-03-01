import cv2
import sys
import numpy as np
import math
import time

def get_countour_area(contour):
    global minarea
    global maxarea
    area = cv2.contourArea(contour)
    if minarea < area < maxarea:
        return area
    return 0

def euclidean_dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def imgtoblob(mask_img):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))

    erosion = cv2.erode(mask_img, kernel)

    closing = cv2.morphologyEx(mask_img, cv2.MORPH_CLOSE, kernel)
    #cv2.imshow("STEP 1", closing)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
    #cv2.imshow("STEP 2", opening)
    dilation = cv2.dilate(opening, kernel, iterations = 3)
    #cv2.imshow("STEP 3", dilation)
    #retbins, bins = cv2.threshold(dilation, 220, 255, cv2.THRESH_BINARY)

    return(dilation)

def clean_and_save_words(data, total_frame, height, width):
    img = np.ones((height, width))

    for word in data:
        for i in range(len(word) - 1):
            if euclidean_dist(*word[i], *word[i-1]) < 40:
                img = cv2.line(img, word[i], word[i+1], 0, 6)
    if len(sys.argv) == 2:
        img = np.array(img, dtype = np.uint8)
        orig_img = cv2.imread(sys.argv[1])
        img = cv2.bitwise_and(orig_img, orig_img, mask = img)
    else:
        img = img * 255
    cv2.imwrite('written_words.jpg', img)
    cv2.imshow('written_words', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def draw():
    minarea = 500
    maxarea = 1000

    cap = cv2.VideoCapture(0)
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = False)

    sensitivity = 20

    green_lower_bound = np.array([60 - sensitivity, 100, 50])
    green_upper_bound = np.array([60 + sensitivity, 255, 255])

    blue_lower_bound = np.array([120 - sensitivity, 100, 50])
    blue_upper_bound = np.array([120 + sensitivity, 255, 255])

    if(cap.isOpened() == False):
    	print('Error opening video stream or file')

    data_writer = open('data.txt', 'w')

    green_prev_loc = (0,0)
    blue_prev_loc = (0,0)
    green_avg_pos = (0,0)

    green_history = 0 #counts number of frames a moving green object was detected
    blue_history = 0 #counts number of frames a moving blue object was detected
    done_counter = 0

    data_points = []

    pen_down_counter = 0
    pen_up_counter = 0
    word = -1
    start_time = time.time()
    radius = 75
    tracked_frame = []
    history = 3
    if len(sys.argv) == 2:
        total_frame = cv2.imread(sys.argv[1])
        height, width = total_frame.shape[:-1]
    else:
        height, width = 800, 1000
        total_frame = np.ones(shape = (height, width, 3))
    saved_frame = np.copy(total_frame)
    while(cap.isOpened()):
        ret, frame = cap.read()
        cam_h = frame.shape[0]
        cam_w = frame.shape[1]

        if ret == True:
            fgmask = fgbg.apply(frame) #create a mask that has the foreground
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convert image to HSV
            masked_img = cv2.bitwise_and(hsv_frame, hsv_frame, mask = fgmask) #separate foreground from background

            green_mask = cv2.inRange(hsv_frame, green_lower_bound, green_upper_bound) #create a mask that has green pixels
            blue_mask = cv2.inRange(hsv_frame, blue_lower_bound, blue_upper_bound) #create a mask that has blue pixels

            green_masked_img = cv2.bitwise_and(masked_img, masked_img, mask = green_mask) #separate green pixels
            blue_masked_img = cv2.bitwise_and(masked_img, masked_img, mask = blue_mask) #separate blue pixels

            green_masked_img = cv2.cvtColor(green_masked_img, cv2.COLOR_HSV2BGR)
            green_masked_img = cv2.cvtColor(green_masked_img, cv2.COLOR_BGR2GRAY)
            blue_masked_img = cv2.cvtColor(blue_masked_img, cv2.COLOR_HSV2BGR)
            blue_masked_img = cv2.cvtColor(blue_masked_img, cv2.COLOR_BGR2GRAY)

            green_mask = imgtoblob(green_masked_img) #reduce noise
            blue_mask = imgtoblob(blue_masked_img) #reduce noise

            _, green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.RETR_TREE) #create contours for green objects
            _, blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.RETR_TREE) #create contours for blue objects

            if green_contours: #find the biggest green object
                green_history += 1
                green_max_box = max(green_contours, key = get_countour_area)

                temp = cv2.moments(green_max_box)
                green_cx = int(temp['m10'] / temp['m00']) #location of x coordinate of centroid
                green_cy = int(temp['m01'] / temp['m00']) #location of y coordinate of centroid

            else:
                green_cx,green_cy = green_avg_pos
                green_history = 0

            if blue_contours: #find the biggest blue object
                blue_history += 1
                blue_max_box = max(blue_contours, key = get_countour_area)

                temp = cv2.moments(blue_max_box)
                blue_cx = int(temp['m10'] / temp['m00']) #location of x coordinate of centroid
                blue_cy = int(temp['m01'] / temp['m00']) #location of y coordinate of centroid

                blue_prev_loc = (blue_cx, blue_cy)
            else:
                blue_cx, blue_cy = blue_prev_loc
                blue_history = 0

            if time.time() - start_time < 1:
                green_avg_pos = (green_cx, green_cy)

            if euclidean_dist(green_cx, green_cy, *green_avg_pos) < radius:
                if len(tracked_frame) == history:
                    tracked_frame = tracked_frame[1:] + [(green_cx, green_cy)]
                else:
                    tracked_frame.append((green_cx, green_cy))

                green_avg_pos = (sum([i[0] for i in tracked_frame])/len(tracked_frame), sum(i[1] for i in tracked_frame)/len(tracked_frame))

                dist = euclidean_dist(blue_cx, blue_cy, green_cx, green_cy)

                if pen_down_counter >= 20 and pen_up_counter >= 20:
                    word += 1
                    data_points.append([])
                    pen_down_counter = 0
                    pen_up_counter = 0

                if dist >= 50 and time.time():
                    pen_up_counter += 1
                    done_counter = 0
                    total_frame = np.copy(saved_frame)
                    data_writer.write("{} {}\n".format(int(width - width * green_cx / cam_w), int(height * green_cy / cam_h)))
                    cv2.drawMarker(total_frame, (int(width - width * green_cx / cam_w), int(height * green_cy / cam_h)), (0, 0, 0), cv2.MARKER_STAR, markerSize=2, thickness=1, line_type=cv2.LINE_AA)
                    cv2.imshow('Image', total_frame)
                    saved_frame = np.copy(total_frame)
                    if word >= 0:
                        data_points[word].append((int(width - width * green_cx / cam_w), int(height * green_cy / cam_h)))

                saw_green = green_history >= 5 #saw a green image for more than 5 frames
                saw_blue = blue_history >= 5 #saw a blue image for more than 5 frames

                if dist <= 50 and saw_blue & saw_green: #if blue and green were correctly tracked and they are close together, exit
                    pen_down_counter += 1
                    if (green_cy >= frame.shape[0] - frame.shape[0]*.1):
                        done_counter += 1
                    if done_counter > 20:
                        break
                    cv2.drawMarker(total_frame, (int(width - width * green_cx / cam_w), int(height * green_cy / cam_h)) , (0, 255, 0), cv2.MARKER_STAR, markerSize=2, thickness=4, line_type=cv2.LINE_AA)
                    cv2.imshow('Image', total_frame)

                # cv2.drawMarker(frame, (int(green_cx), int(green_cy)), (0, 0, 255), cv2.MARKER_STAR, markerSize=4, thickness=4, line_type=cv2.LINE_AA)
                # cv2.drawMarker(frame, (int(blue_cx), int(blue_cy)), (0, 255, 0), cv2.Mcheck_hARKER_STAR, markerSize=4, thickness=4, line_type=cv2.LINE_AA)

            # cv2.imshow('img', frame)
            # cv2.imshow('mask', green_mask)
            # cv2.imshow('bmast', blue_mask)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break


    cap.release()
    cv2.destroyAllWindows()
    clean_and_save_words(data_points, total_frame, height, width)
