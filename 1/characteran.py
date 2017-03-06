import cv2
import numpy as np

def findOuterBoxMask(contours, hierarchy, thresh):
    min_parent_are = 100 * 100 * 0.10
    winningIndex = -1
    winningParentId = -1
    bestCharCount = 0
    lowestArea = 99999999999

    charsRecognizedInContours = np.zeros(len(contours))

    charsRecognized = 0

    parentId = -1

    hasParent = False

    bestParentId = -1
    i = 0
    while(i < len(contours)):
        charsRecognized = charsRecognized + 1
        parentId = hierarchy[i][3]
        hasParent = True
        charsRecognizedInContours[parentId] = + charsRecognizedInContours[parentId] + 1
        j = 0
        while(j < len(contours)):
            if(charsRecognizedInContours[i] > charsRecognized):
                charsRecognized = charsRecognizedInContours[i]
                bestParentId = i
            j = j + 1

        boxarea = cv2.contourArea()
        if(boxarea < min_parent_are):
            continue
        if((charsRecognized > bestCharCount) or (charsRecognized == bestCharCount and boxarea < lowestArea)):
            bestCharCount = charsRecognized
            winningIndex = i
            winningParentId = bestParentId
            lowestArea = boxarea

    if(winningIndex != -1 and bestCharCount >=3):

