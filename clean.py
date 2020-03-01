import numpy as np
import cv2
import math

# data_points = []
# for line in open('data.txt', 'r').readlines():
#     y,x = line.split()
#     data_points.append((int(x), int(y)))
#
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
# image = np.ones(shape = (577, 1400))
# image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
# #cv2.imshow("STEP 1", closing)
# image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
# for i in range(len(data_points)-1):
#     image = cv2.line(image, (0,0), (300,300), 0, 6)
#
# image = cv2.dilate(image, kernel, iterations = 3)
# cv2.imshow('img', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

def euclidean_dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

img = np.ones((577,1400))
data = []
for line in open('data.txt', 'r'):
    x,y = line.split()
    cv2.drawMarker(img, (int(x),int(y)), 0, cv2.MARKER_STAR, markerSize=4, thickness=4, line_type=cv2.LINE_AA)
    # data.append((int(x), int(y)))

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
# img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
img = cv2.dilate(img, kernel, iterations = 1)




# avg_dist = sum([euclidean_dist(*data[i], *data[i+1]) for i in range(len(data)-1)])/len(data)
# lower_bound = 0
# upper_bound = len(data)
# for i in range(1, len(data) - 1):
#     if euclidean_dist(*data[i], *data[i+1]) > 2.5 * avg_dist:
#         lower_bound = i+1

# print(lower_bound, upper_bound)
# data = data[lower_bound:upper_bound]
#
# for i in range(len(data) - 1):
#     img = cv2.line(img, data[i], data[i+1], 0, 6)

# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
