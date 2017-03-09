import cv2
import detector
import bin
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
        bin_img = bin.Wolf(imgplate, 1, 18, 18, 0.05 + (k * 0.35), 128)
        bin_img = cv2.bitwise_not(bin_img)
        cv2.imshow('plate', bin_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


else:
    print("no plate")