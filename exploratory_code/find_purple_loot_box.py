import cv2
import numpy as np
import imutils


def find(img):

   hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

   lower_range = np.array([110,50,50])
   upper_range = np.array([130,255,255])

   mask = cv2.inRange(hsv, lower_range, upper_range)

   cv2.imshow('image', img)
   cv2.imshow('mask', mask)

while(True):
   screen = np.array(ImageGrab.grab())
   k = cv2.waitKey(5) & 0xFF
   if k == 27:
      break

cv2.destroyAllWindows()