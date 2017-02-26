import cv2
import numpy as numpy
img = cv2.imread('2.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img = cv2.GaussianBlur(gray,(3,3),0)
sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)  # x
sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)  # y
edges = cv2.Canny(img,100,200)

cv2.imshow("1a", sobelx)
cv2.imshow("1b", sobely)
cv2.imshow("1c", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()