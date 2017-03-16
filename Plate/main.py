import cv2
import detector
import bin
import textcontours

img = cv2.imread('1.jpg')
print img.shape[1]
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

im_sum, im_sum_sq = cv2.integral2(img_gray, sqdepth=cv2.CV_64F)
im_sum.itemset((100, 100), 12)
print im_sum.item(100, 100)

imgplates = detector.detect(img)
if len(imgplates) != 0:
    for imgplate in imgplates:
        k = 0
        cv2.imshow('just', imgplate)
        bin_img = bin.Wolf(imgplate, 3, 18, 18, 0.05 + (k * 0.35), 128)
        bin_img = cv2.bitwise_not(bin_img)
        contours = textcontours.getTextContours(bin_img)
        # cv2.drawContours(bin_img, contours, -1, (0,255,0), 1)
        textcontours.drawContours(bin_img, contours)
        cv2.imshow('plate', bin_img)
        print textcontours.height
    cv2.waitKey(0)
    cv2.destroyAllWindows()


else:
    print("no plate")