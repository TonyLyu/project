import cv2
import numpy as np
import bin
import textcontours


def characteranalysis(img):
    k = 0
    bin_img = bin.Wolf(img, 3, 18, 18, 0.05 + (k * 0.35), 128)
    bin_img = cv2.bitwise_not(bin_img)
    tc = textcontours(bin_img, img)

def filter(threshold, tc):
    rows, cols = threshold.shape[:2]
    starting_min_height = round(rows * 0.3)
    starting_max_height = round(rows * (0.3 + 0.2))
    height_step = round(rows * 0.1)
    num_steps = 4
    bestFitScore = -1
    for i in range(0, num_steps):
        for z in range(0, len(tc)):
            k = 0

def filterByBoxSize(tc, minHeightPx, maxHeightPx):
    larger_char_height_mm = 70.0
    larger_char_width_mm = 35.0
    idealAspect = larger_char_width_mm / larger_char_height_mm
    aspecttolerance = 0.25
    for i in range(0, len(tc)):
        if tc.goodIndices[i] == False:
            continue
        tc.goodIndices[i] == False
        x, y, width, height = cv2.boundingRect(tc.contours[i])
        minWidth = height * 0.2

# def findOuterBoxMask(contours, hierarchy, thresh):
#     min_parent_are = 100 * 100 * 0.10
#     winningIndex = -1
#     winningParentId = -1
#     bestCharCount = 0
#     lowestArea = 99999999999
#
#     charsRecognizedInContours = np.zeros(len(contours))
#
#     charsRecognized = 0
#
#     parentId = -1
#
#     hasParent = False
#
#     bestParentId = -1
#     i = 0
#     while(i < len(contours)):
#         charsRecognized = charsRecognized + 1
#         parentId = hierarchy[i][3]
#         hasParent = True
#         charsRecognizedInContours[parentId] = + charsRecognizedInContours[parentId] + 1
#         j = 0
#         while(j < len(contours)):
#             if(charsRecognizedInContours[i] > charsRecognized):
#                 charsRecognized = charsRecognizedInContours[i]
#                 bestParentId = i
#             j = j + 1
#
#         boxarea = cv2.contourArea()
#         if(boxarea < min_parent_are):
#             continue
#         if((charsRecognized > bestCharCount) or (charsRecognized == bestCharCount and boxarea < lowestArea)):
#             bestCharCount = charsRecognized
#             winningIndex = i
#             winningParentId = bestParentId
#             lowestArea = boxarea
#
#     if(winningIndex != -1 and bestCharCount >=3):

