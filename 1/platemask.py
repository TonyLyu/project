import cv2
import numpy as np

class platemask:
    def __init__(self, thresholds):
        self.hasplatemask = False
        self.thresholds = thresholds
    def getMask(self):
        return self.platemask
    def findOuterBoxMask(self, contours):

        min_parent_area = 100 * 100 * 0.10
        winningIndex = -1
        winningParentId = -1
        bestCharCount = 0
        lowestArea = 99999999999

        for imgIndex in range(0, len(contours)):
            charsRecognized = 0

            parentId = -1

            hasParent = False

            bestParentId = -1
            charsRecognizedInContours = np.zeros(len(contours[imgIndex]).goodIndices)
            for i in range(0, len(contours[imgIndex].goodIndices)):
                if contours[imgIndex].goodIndices[i]:
                    charsRecognized += 1
                if contours[imgIndex].goodIndices[i] and contours[imgIndex].hierarchy[i][3] != -1:
                    parentId = contours[imgIndex].hierarchy[i][3]
                    hasParent = True
                    charsRecognizedInContours[parentId] += 1
            if charsRecognized == 0:
                continue
            if hasParent:
                charsRecognized = 0
            for i in range(0, len(contours[imgIndex].goodIndices)):
                if charsRecognizedInContours[i] > charsRecognized:
                    charsRecognized = charsRecognizedInContours[i]
                    bestParentId = i
            boxarea = cv2.contourArea(contours[imgIndex].contours[bestParentId])
            if boxarea < min_parent_area:
                continue
            if charsRecognized > bestCharCount or (charsRecognized == bestCharCount and boxarea < lowestArea):
                bestCharCount = charsRecognized
                winningIndex = imgIndex
                winningParentId = bestParentId
                lowestArea = boxarea
        if winningIndex != -1 and bestCharCount >= 3:
            mask = np.zeros(len(self.thresholds[winningIndex]), dtype = "unit8")
            cv2.drawContours(mask, contours[winningIndex].contours, winningParentId,
                             (255, 255, 255),cv2.FILLED, 8, contours[winningIndex].hierarchy,
                             0)
            morph_elem = 2
            morph_size = 3
            element = cv2.getStructuringElement(morph_elem,
                                                (2 * morph_size + 1, 2 * morph_size + 1),
                                                (morph_size, morph_size))
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, element)
            contoursSecondRound = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            biggestContourIndex = -1
            largesArea = 0.0




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
#

