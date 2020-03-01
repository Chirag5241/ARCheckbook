from check import get_check
import multiword
import test
import cv2
import time
import os
import numpy as np

def run_check_demo():
	error = 1
	while error:
		try:
			multiword.main("", "Recipient Name: ")
			name = test.main()
			print(name)
			error = 0
		except:
			print("Try again")

	error = 1
	while error:
		try:
			multiword.main("", "Memo Line: ")
			memo = test.main()
			print(memo)
			error = 0
		except:
			print("Try again")

	error = 1
	while error:
		try:
			multiword.main("", "Amount of Money: ")
			amount = int(test.main())
			print(amount)
			error = 0
		except:
			print("Try again")

	get_check(name, memo, amount)

	filled_check = cv2.imread('written_words.jpg')
	cv2.imshow('check', filled_check)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def run_sign_demo():
	multiword.main("img.jpg", "")
	filled_check = cv2.imread('written_words.jpg')

	cv2.imshow('check', filled_check)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def run_draw_demo():
	multiword.main("", "Draw Anything:")
	drawn_img = cv2.imread('written_words.jpg')

	cv2.imshow('check', drawn_img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
