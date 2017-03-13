import cv2
import textcontours
import math
class CharPointInfo:
    def __init__(self, contour, index):
        self.contourIndex = index
        self.bx, self.by, self.bw, self.bh= cv2.boundingRect(contour)
        x = self.bx + int(self.bw / 2)
        y = self.by
        self.top = (x, y)
        x = self.bx + int(self.bw / 2)
        y = self.by + self.bh
        self.bottom = (x, y)

class LineFinder:
    def __init__(self, image):
        self.image = image

    def findLines(self, image, contours):
        min_area_to_ignore = 0.65
        linesFound = []
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        charPoints = []
        for i in range(0, len(contours)):
            if contours.goodIndices[i] == False:
                continue
            charPoint = CharPointInfo(contours.contours[i], i)
            charPoints.append(charPoint)
        bestCharArea = self.getBestLine(contours, charPoints)
        bestLine = self.extendToEdges(contours.width, contours.height, bestCharArea)
        if len(bestLine) > 0:
            linesFound.append(bestLine)
        return linesFound

    def getBestLine(self, contours, charPoints):
        bestStripe = []
        if(len(charPoints) <= 1):
            return bestStripe
        charhights = []
        for i in range(0, len(charPoints)):
            charhights.append(charPoints[i].bh)
        medianCharHeight = self.median(charhights, len(charhights))
        topLines = []
        bottomLines = []
        for i in range(0, len(charPoints)-1):
            for k in range(i+1, len(charPoints)):
                if charPoints[i].top[0] < charPoints[k].top[0]:
                    leftCPIndex = i
                    rightCPIndex = k
                else:
                    leftCPIndex = k
                    rightCPIndex = i
                top = LineSegment(charPoints[leftCPIndex].top, charPoints[rightCPIndex].top)
                bottom = LineSegment(charPoints[leftCPIndex].bottom, charPoints[rightCPIndex].bottom)
                parallelBot = top.getParalleLine(medianCharHeight * -1)
                parallelTop = bottom.getParalleLine(medianCharHeight)
                if abs(top.angle) <= 15 and abs(parallelBot.angle) <= 15:
                    topLines.append(top)
                    bottomLines.append(parallelBot)
                if abs(parallelTop.angle) <= 15 and abs(bottom.angle) <= 15:
                    topLines.append(parallelTop)
                    bottomLines.append(bottom)
        bestScoreIndex = 0
        bestScore = -1
        bestScoreDistance = -1
        for i in range(0, len(topLines)):
            scoring_min_threshold = 0.97
            scoring_max_threshold = 1.03
            curScore = 0
            for charidx in range(0, len(charPoints)):
                topYPos = topLines[i].getPointAt(charPoints[charidx].top[0])
                botYPos = bottomLines[i].getPointAt(charPoints[charidx].bottom[0])
                minTop = charPoints[charidx].top[1] * scoring_min_threshold
                maxTop = charPoints[charidx].top[1] * scoring_max_threshold
                minBot = (charPoints[charidx].bottom[1]) * scoring_min_threshold
                maxBot = (charPoints[charidx].bottom[1]) * scoring_max_threshold
                if (topYPos >= minTop and topYPos <= maxTop) and (botYPos >= minBot and botYPos <= maxBot):
                    curScore += 1
            if (curScore > bestScore) or (curScore == bestScore and topLines[i].length > bestScoreDistance):
                bestScore = curScore
                bestScoreIndex = i
                bestScoreDistance = topLines[i].length
        if bestScore < 0:
            return
        bestStripe.append(topLines[bestScoreIndex].p1)
        bestStripe.append(topLines[bestScoreIndex].p2)
        bestStripe.append(bottomLines[bestScoreIndex].p1)
        bestStripe.append(bottomLines[bestScoreIndex].p2)

        return bestStripe



    def extendToEdges(self, width, height, charArea):
        extended = []
        if(len(charArea) < 4):
            return extended
            top = LineSegment(charArea[0], charArea[1])
            bottom = LineSegment(charArea[3], charArea[4])
            topLeft = (0, top.getPointAt(0))
            topRight = (width, top.getPointAt(width))
            bottomRight = (width, bottom.getPointAt(width))
            bottomLeft = (0, bottom.getPointAt(0))
        extended.append(topLeft)
        extended.append(topRight)
        extended.append(bottomRight)
        extended.append(bottomLeft)

        return extended



    def median(self, array, arraySize):
        if arraySize == 0:
            return 0
        array = sorted(array)
        if arraySize % 2 ==1:
            return array[arraySize / 2]
        else:
            return  array[arraySize / 2 - 1] + array[arraySize / 2] / 2
class LineSegment:
    def __init__(self):
        self.init(0, 0, 0, 0)
    def __init__(self, p1, p2):
        self.init(p1[0], p1[1], p2[0], p2[1])
    def __init__(self, x1, y1, x2, y2):
        self.init(x1, y1, x2, y2)
    def init(self, x1, y1, x2, y2):
        self.p1 = (x1, y1)
        self.p2 = (x2, y2)
        if self.p2[0] - self.p1[0] == 0:
            self.slope = 0.00000000001
        else:
            self.slope = float(self.p2[1] - self.p1[1]) / float(self.p2[0] - self.p2[0])
        self.length = distanceBetweenPoints(self.p1, self.p2)
        self.angle = angleBetweenPoints(self.p1, self.p2)
    def getParalleLine(self, distance):
        diff_x = self.p2[0] - self.p1[0]
        diff_y = self.p2[1] - self.p1[1]
        angle = math.atan2(diff_x, diff_y)
        dist_x = distance - math.cos(angle)
        dist_y = distance - math.sin(angle)
        offsetX = int(round(dist_x))
        offsetY = int(round(dist_y))
        result = LineSegment(self.p1[0] + offsetX, self.p1[1] + offsetY,
                             self.p2[0] + offsetX, self.p2[1] + offsetY)
        return result
    def getPointAt(self, x):
        return self.slope * (x - self.p2[1]) + self.p2[1]

def distanceBetweenPoints(p1, p2):
    asquared = float(p2[0] - p1[0]) * (p2[0] - p1[0])
    bsquared = float(p2[1] - p1[1]) * (p2[1] - p1[1])
    return math.sqrt(asquared + bsquared)

def angleBetweenPoints(p1, p2):
    deltaY = int(p2[1] - p1[1])
    deltaX = int(p2[0] - p1[0])
    return math.atan2(float(deltaY), float(deltaX) * (180 / math.pi)
    )