import numpy as np
import cv2
import preprocess
import segment as se
from matplotlib import pyplot as plt

def binarization(original_image):
    # height, width, colorchannel = original_image.shape
    # imgHSV = np.zeros((height, width, 3), np.uint8)

    # imgHSV = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    #img,tsh = preprocess.preprocess(original_image)
    #img = cv2.medianBlur(original_image, 5)
    #th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    blur = cv2.GaussianBlur(original_image, (5, 5), 0)
    ret2, th2 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV+ cv2.THRESH_OTSU)

    return th2
ori_img = cv2.imread('imgplate.png', 0)
gray_img = cv2.imread('imgplate.png',0)
bin_img = binarization(gray_img)
cv2.imshow('2', bin_img)

hsv = cv2.cvtColor(ori_img, cv2.COLOR_BGR2HSV)
M = cv2.calcH
hist_full = cv2.calcHist([gray_img],[0],None,[256],[0,256])
plt.plot(hsv)
plt.show()
#seg = se.segm(bin_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
