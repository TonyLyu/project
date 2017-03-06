import cv2
import detector

img = cv2.imread('2.png')
imgplates = detector.detect(img)
if len(imgplates) != 0:
    for imgplate in imgplates:
        cv2.imshow('plate', imgplate)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
else:
    print("no plate")