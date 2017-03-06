import cv2
import numpy as np
import math

def calcLocalStats(im, map_m, map_s, winx, winy):
    rows, cols = im.shape
    im_sum, im_sum_sq = cv2.integral2(im, sqdepth=cv2.CV_64F)
    wxh = winx/2
    wyh = winy/2
    x_firstth = wxh
    y_lastth = rows - wyh - 1;
    y_firstth = wyh
    winare = winx * winy

    max_s = 0
    j = y_firstth
    while(j <= y_lastth):
        sum = sum_q = 0
        sum = im_sum.item(j-wyh+winy, winx) - im_sum.item(j-wyh, winx) - im_sum.item(j-wyh+winy, 0) + im_sum.item(j-wyh, 0)
        sum_sq = im_sum_sq.item(j-wyh+winy, winx) - im_sum-sq.item(j-wyh, winx) - im_sum_sq.item(j-wyh+winy, 0) + im_sum_sq.item(j-wyh, 0)
        m = sum / winare
        s = math.sqrt((sum_sq - m * sum)/winare)

        map_m.fset(x_firstth, j, m)
        j = j + 1
    return 0

def NSW(img, version, winx, winy, k, dR):
    rows, cols = img.shape[:2]
    map_m = np.zeros((rows, cols, 1), cv2.CV_32F)
    map_S = np.zeros((rows, cols, 1), cv2.CV_32F)
def otsu(img):
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return th3