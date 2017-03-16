import cv2
from scorekeeper import ScoreKeeper
from textlinecollection import TextLineColeection
from linefinder import LineSegment, distanceBetweenPoints
class PlateCorners:
    def __init__(self, inputImage, plateLines, img_data, textLines):
        self.tlc = TextLineColeection(textLines)
        self.img_data = img_data
        self.inputImage = inputImage
        self.plateLines = plateLines
        self.textLines = textLines
        self.bestHorizontalScore = 999999999
        self.bestVerticalScore = 99999999
        self.bestTop = LineSegment()
        self.bestBottom = LineSegment()
        self.bestLeft = LineSegment()
        self.bestRight = LineSegment()



    def findPlateCorners(self):
        horizontalLines = len(self.plateLines.horizontalLines)
        verticalLines = len(self.plateLines.verticalLines)
        for h1 in range(-1, horizontalLines):
            for h2 in range(-1, horizontalLines):
                if h1 == h2 and h1 != -1:
                    continue
                self.scoreHorizontals(h1, h2)
        for v1 in range(-1, verticalLines):
            for v2 in range(-1, verticalLines):
                if v1 == v2 and v1 != -1:
                    continue
                self.scoreHorizontals(v1, v2)
        if self.bestLeft.p1[0] == 0 and self.bestLeft.p1[1] ==0 and self.bestLeft.p2[0] == 0 and self.bestLeft.p2[1]:
            self.img_data.disqualified = True
        elif self.bestTop.p1[0] == 0 and self.bestTop.p1[1] ==0 and self.bestTop.p2[0] == 0 and self.bestTop.p2[1]:
            self.img_data.disqualified = True
        corners = []
        corners.append(self.bestTop.intersection(self.bestLeft))
        corners.append(self.bestTop.intersection(self.bestRight))
        corners.append(self.bestBottom.intersection(self.bestRight))
        corners.append(self.bestTop.intersection(self.bestLeft))

        return corners

    def scoreVerticals(self, v1, v2):
        scoreKeeper = ScoreKeeper()
        left = LineSegment()
        right = LineSegment()
        charHeightToPlateWidthRatio = 304.8 / 70
        idealPixelWidth = self.tlc.charHeight * (charHeightToPlateWidthRatio * 1.03)
        confidenceDiff = 0
        missingSegmentPenalty = 0

        if v1 == -1 and v2 == -1:
            left = self.tlc.centerVerticalLine.getParalleLine(-1 * idealPixelWidth / 2)
            right = self.tlc.centerVerticalLine.getParalleLine(idealPixelWidth / 2)
            missingSegmentPenalty = 2
            confidenceDiff += 2
        elif v1 != -1 and v2 != -1:
            left = self.plateLines.verticalLines[v1].line
            right = self.plateLines.verticalLinesp[v2].line
            confidenceDiff += (1.0 - self.plateLines.verticalLines[v1].confidence)
            confidenceDiff += (1.0 - self.plateLines.verticalLines[v2].confidence)
        elif v1 == -1 and v2 != -1:
            right = self.plateLines.verticalLinesp[v2].line
            left = right.getParalleLine(idealPixelWidth)
            missingSegmentPenalty += 1
            confidenceDiff += (1.0 - self.plateLines.verticalLines[v2].confidence)
        elif v1 != -1 and v2 == -1:
            left = self.plateLines.verticalLines[v1].line
            right = left.getParalleLine(-1 * idealPixelWidth)
            missingSegmentPenalty += 1
            confidenceDiff += (1.0 - self.plateLines.verticalLines[v1].confidence)
        scoreKeeper.setScore("SCORING_LINE_CONFIDENCE_WEIGHT",confidenceDiff, 18.0)
        scoreKeeper.setScore("SCORING_MISSING_SEGMENT_PENALTY_VERTICAL", missingSegmentPenalty, 10)
        if self.tlc.isLeftOfText(left) < 1 or tlc.isLeftOfText(right) > -1:
            return Nnoe
        perpendicularCharAngle = tlc.charAngle - 90
        charanglediff = abs(perpendicularCharAngle - left.angle)
        scoreKeeper.setScore("SCORING_ANGLE_MATCHES_LPCHARS_WEIGHT", charanglediff, 1.1)
        leftMidLinePoint = left.closestPointOnSegmentTo(self.tlc.centerVerticalLine.midpoint())
        rightMidLinePoint = right.closestPointOnSegmentTo(self.centerHorizontalLine.midpoint())
        actual_width = distanceBetweenPoints(leftMidLinePoint, rightMidLinePoint)
        if actual_width < (idealPixelWidth / 4):
            return None
        plateDistance = abs(idealPixelWidth - actual_width)
        plateDistance = plateDistance / float(inputImage.shape[1])
        scoreKeeper.setScore("SCORING_DISTANCE_WEIGHT_VERTICAL",plateDistance, 4.0)
        score = scoreKeeper.getTotal()
        if score < self.bestVerticalScore:
            self.bestVerticalScore = score
            self.bestLeft = LineSegment(left.p1[0], left.p1[1], left.p2[0], left.p2[1])
            self.bestLeft = LineSegment(right.p1[0], right.p1[1], right.p2[0], right.p2[1])
