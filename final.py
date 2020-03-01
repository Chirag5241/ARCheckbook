from check import get_check
import cv2
import time
import numpy as np

name = "None"
description = "None"
money = 1
def name_keyboard():
	name = input("Enter your name : ") 
	return(name)

def description_keyboard():
	description = input("Enter the description : ") 
	return(description)


def money_keyboard():
	money = input("Enter the amount : ") 
	return(money)

cap = cv2.VideoCapture(0)

k_enable = 0

while True:

	ret, frame = cap.read()  
	if ret == True:

		cv2.putText(frame, "Please Draw Your Name :",(10,70), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 100), 4)
		cv2.putText(frame, "Press k to move to keyboard :",(10,675), cv2.FONT_HERSHEY_TRIPLEX, 1, (100, 0, 255), 2)
		cv2.putText(frame, "Press q to quit :",(10,700), cv2.FONT_HERSHEY_TRIPLEX, 1, (100, 0, 255), 2)
		pts = np.array([[1100,600],[1250,600],[1250,700],[1100,700]], np.int32)
		cv2.fillPoly(frame, np.int_([pts]), (0, 0, 10))
		cv2.imshow('LIVE FEED',frame) 

		if cv2.waitKey(1) & 0xFF == ord('k'):
			k_enable = 1
			break
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else :
		break


cv2.destroyAllWindows()
cv2.waitKey(1)
cap.release()

if k_enable == 1:
	name = name_keyboard()

description = description_keyboard()
money = money_keyboard()

print (name) 
print (description) 
print (money) 
print("Preparing Check")
get_check(name,description,money)


img = cv2.imread('image.png')#jpg
cv2.imshow('Check',img)
while cv2.waitKey(1) & 0xFF != ord('q'):
	continue
cv2.destroyAllWindows()


