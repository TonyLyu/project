import cv2
import preprocess as pre
import platedetect as pld
import DetectChars as DC
import PossiblePlate
import PossibleChar

SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)
showSteps = False

def main():
    blnKNNTrainingSuccessful = DC.loadKNNDataAndTrainKNN()
    if blnKNNTrainingSuccessful == False:  # if KNN training was not successful
        print "\nerror: KNN traning was not successful\n"  # show error message
        return  # and exit program
        # end if
    original_image = cv2.imread("2.png", 1)
    imgGrayScale, imgThresh = pre.preprocess(original_image)
    cv2.imshow('gray', imgGrayScale)
    cv2.imshow('thresh', imgThresh)
    listOfPossiblePlates = pld.detectPlates(imgThresh, original_image)
    listOfPossiblePlates = DC.detectCharsInPlates(listOfPossiblePlates)
    if len(listOfPossiblePlates) == 0:
        print "no license plates"
    else:
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse=True)
        licPlate = listOfPossiblePlates[0]
        cv2.imshow('imgPlate', licPlate.imgPlate)
        cv2.imwrite('imgplate.png', licPlate.imgPlate)


    cv2.imshow("1a", imgGrayScale)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()