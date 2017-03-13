import cv2
import numpy as np
import bin
import textcontours
import platemask
import linefinder

def characteranalysis(img):
    k = 0
    bin_img = bin.Wolf(img, 3, 18, 18, 0.05 + (k * 0.35), 128)
    bin_img = cv2.bitwise_not(bin_img)
    allTextContours = []
    for i in range(0, len(bin_img)):
        tc = textcontours(bin_img, img)
        allTextContours.append(tc)
    for i in range(0, len(bin_img)):
        # some problems
        tc = filter(bin_img, allTextContours[i])

    plateMask = platemask(bin_img)
    plateMask.findOuterBoxMask(allTextContours)
    hasPlateBorder = plateMask.hasplatemask
    plateBorderMask = plateMask.getMask()
    if plateMask.hasplatemask:
        for i in range(0, len(bin_img)):
            allTextContours[i] = filterByOuterMask(allTextContours[i])
    bestFitScore = -1
    bestFitIndex = -1
    for i in range(0, len(bin_img)):
        segmentCount = allTextContours[i].getGoodIndicesCount()
        if segmentCount > bestFitScore:
            bestFitScore = segmentCount
            bestFitIndex = i
            bestThreshold = bin_img[i]
            bestContours = allTextContours[i];
    if bestFitScore <= 1:
        print "low best fit score"
    img_contours = bestContours.drawContours()
    cv2.imshow("Matching Contours", img_contours)
    lf = linefinder.LineFinder(img)
    linePolygons = lf.findLines(bin_img, bestContours)
    tempTextLines = []
    for i in range(0, len(linePolygons)):
        linePolygon = linePolygons[i]
        topLine = linefinder.LineSegment(linePolygon[0][0], linePolygons[0][1],
                                         linePolygon[1][0], linePolygon[1][1])
        bottomLine = linefinder.LineSegment(linePolygon[3][0], linePolygons[3][1],
                                            linePolygon[2][0], linePolygon[2][1])
        textArea = getCharArea(topLine, bottomLine, bestContours)

        
    return bin_img

def filter(threshold, tc):
    rows, cols = threshold.shape[:2]
    starting_min_height = round(rows * 0.3)
    starting_max_height = round(rows * (0.3 + 0.2))
    height_step = round(rows * 0.1)
    num_steps = 4
    bestFitScore = -1
    for i in range(0, num_steps):
        for z in range(0, len(tc)):
            tc.goodIndices[z] = True
        tc = filterByBoxSize(tc, starting_min_height + (i * height_step), starting_max_height + (i * height_step))
        goodIndices = tc.getGoodInicesCount()
        if goodIndices == 0 or goodIndices < bestFitScore:
            continue
        tc = filterContourHoles(tc)
        goodIndices = tc.getGoodInicesCount()
        if goodIndices == 0 or goodIndices <= bestFitScore:
            continue
        segmentConut = tc.getGoodInicesCount()
        if segmentConut > bestFitScore:
            bestFitScore = segmentConut
            bestIndices = tc.getIndicesCopy()
    tc.setIndices(bestIndices)
    return tc



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
        if height >= minHeightPx and height <= maxHeightPx and width > minWidth:
            charAspect = float(width) / float (height)
            if abs(charAspect - idealAspect) < aspecttolerance:
                tc.goodIndices[i] = True

    return tc

def filterContourHoles(tc):
    for i in range(0, len(tc)):
        if tc.goodIndices[i] == False:
            continue
        tc.goodIndices[i] = False
        parentIndex = tc.hierarchy[i][3]
        if parentIndex >= 0 and tc.goodIndices[parentIndex]:
            continue
        else:
            tc.goodIndices[i] = True
    return tc

def filterByOuterMask(textcontours, hasPlateBorder, plateBorderMask):
    minimum_percent_left_after_mask = 0.1
    minium_percent_of_chars_inside_plate_mask = 0.6
    if hasPlateBorder == False:
        return textcontours
    plateMask = plateBorderMask
    tempMaskedContour = np.zeros((plateMask.shape[0],plateMask.shape[1]), dtype="uint8")
    tempFullContour = np.zeros((plateMask.shape[0],plateMask.shape[1]), dtype="uint8")
    charsInsideMask = 0
    totalChars = 0
    originalindices = []
    for i in range(0, len(textcontours)):
        originalindices.append(textcontours.goodIndices[i])
    for i in range(0, len(textcontours)):
        if(textcontours.goodIndices[i] == False):
            continue
        totalChars += 1
        tempFullContour = np.zeros((plateMask.shape[0],plateMask.shape[1]), dtype="uint8")
        cv2.drawContours(tempFullContour, textcontours.contours, i, (255, 255, 255), cv2.FILLED, 8, textcontours.hierarchy)
        plateMask = cv2.bitwise_not(tempFullContour, tempMaskedContour)
        textcontours.goodIndices[i] = False
        beforeMaskWhiteness = cv2.mean(tempFullContour)[0]
        afterMaskWhiteness = cv2.mean(tempMaskedContour)[0]
        if float(afterMaskWhiteness) / beforeMaskWhiteness > minimum_percent_left_after_mask:
            charsInsideMask += 1
            textcontours.goodIndices[i] = True
    if(totalChars == 0):
        textcontours.goodIndices = originalindices
        return textcontours
    percentCharsInsideMask = float(charsInsideMask) / totalChars
    if percentCharsInsideMask < minium_percent_of_chars_inside_plate_mask:
        textcontours.goodIndices = originalindices
        return textcontours

def getCharArea(topLine, bottomLine, bestContours):
    max = 100000
    min = -1
    leftX = max
    rightX = min
    for i in range(0, len(bestContours)):
        if bestContours.goodIndices[i] == False:
            continue
        for z in range(z, len(bestContours.contours[i])):
            if bestContours.contours[i][z][0] < leftX:
                leftX = bestContours.contours[i][z][0]
            if bestContours.contours[i][z][0] > rightX:
                rightX = bestContours.contours[i][z][0]
    charArea = []
    if leftX != max and rightX != min:
        tl = (leftX, topLine.getPointAt(leftX))
        tr = (rightX, topLine.getPointAt(rightX))
        br = (rightX, bottomLine.getPointAt(rightX))
        bl = (leftX, bottomLine.getPointAt(leftX))
        charArea.append(tl)
        charArea.append(tr)
        charArea.append(br)
        charArea.append(bl)
    return charArea
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
