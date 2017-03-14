import cv2
import linefinder
import transformation
import textline


class EdgeFinder:
    def __init__(self, img_data):
        self.img_data = img_data
    def findEdgeCorners(self):
        high_contrast = self.is_high_contrast(self.img_data.crop_gray)
        returnPoints = []
        if high_contrast:

    def detection(self, high_contrast):
        tlc = TextLineColeection(self.img_data.textLines)
        corners = []
        rows, cols = self.img_data.crop_gray.shape
        if(high_contrast):
            expandX = int (float(cols) * 0.5)
            expandY = int(float(rows) * 0.5)
            w = cols
            h = rows

            corners.append(-1 * expandX, -1 * expandY)
            corners.append(expandX + w, -1 * expandY)
            corners.append(expandX + w, expandY + h)
            corners.append(-1 * expandX, expandY + h)
        elif tlc.longerSegment.length > tlc.charHeight * 3:
            charHeightToPlateWidthRatio = 304.8 / 70
            idealPixelWidth = tlc.charHeight * charHeightToPlateWidthRatio

            charHeightToPlateHeightRatio = 152.8 / 70
            idealPixelHeight = tlc.charHeight * charHeightToPlateHeightRatio

            verticalOffset = idealPixelHeight * 1.5 / 2
            horizontaOffset = idealPixelWidth * 1.25 / 2
            topLine = tlc.centerHorizontalLine.getParalleLine(verticalOffset)
            bottomLine = tlc.centerHorizontalLine.getParalleLine(-1 * verticalOffset)

            leftLine = tlc.centerVerticalLine.getParalleLine(-1 * horizontaOffset)
            rightLine = tlc.centerVerticalLine.getParalleLine(horizontaOffset)

            topLeft = topLine.intersection(leftLine)
            topRight = topLine.intersection(rightLine)
            botRight = bottomLine.intersection(rightLine)
            botLeft = bottomLine.intersection(leftLine)

            corners.append(topLeft)
            corners.append(topRight)
            corners.append(botRight)
            corners.append(botLeft)
        else:
            expandX = int(float(cols) * 0.15)
            expandY = int(float(rows) * 0.15)
            w = cols
            h = rows
            corners.append(-1 * expandX, -1 * expandY)
            corners.append(expandX + w, -1 * expandY)
            corners.append(expandX + w, expandY + h)
            corners.append(-1 * expandX, expandY + h)
        width = self.img_data.grayImg.shape[1]
        height = self.img_data.grayImg.shape[0]
        imgTransform = transformation.Transformation(self.img_data.grayImg,
                                                     self.img_data.crop_gray,
                                                     0, 0, width, height)
        remappedCorners = imgTransform.transformSmallPointsTOBigImage(corners)
        cropSize = imgTransform.getCropSize(remappedCorners, (120, 60))
        transmtx = imgTransform.getTransformationMatrix(remappedCorners, cropSize)
        newCrop = imgTransform.crop(cropSize, transmtx)
        newLines = []
        for i in range(0, len(self.img_data.textLines)):
            textArea = imgTransform.transformSmallPointsTOBigImage(self.img_data.textLines[i].textArea)
            linePolygon = imgTransform.transformSmallPointsTOBigImage(self.img_data.textLines[i].linePolygon)
            textAreaRemapped = imgTransform.remapSmallPointstoCrop(textArea, transmtx)
            linePolygonRemapped = imgTransform.remapSmallPointstoCrop(linePolygon, transmtx)
            newLines.append(textline.TextLine(textAreaRemapped, linePolygonRemapped,
                                              newCrop.shape[1], newCrop.shape[0]))
            smallPlateCorners = []
            if high_contrast:
                smallPlateCorners = self.highContrastDetection(newCrop, newLines)
            else:
                smallPlateCorners = self.normalDetection(newCrop, newLines)
    def normalDetection(self, newCrop, newLines):
        


    def highContrastDetection(self, newCrop, newLines):
        smallPlateCorners = []

        morph_size = 3
        closureElement = cv2.getStructuringElement(2, (2 * morph_size + 1, 2 * morph_size + 1), (morph_size, morph_size))
        newCrop = cv2.morphologyEx(newCrop, cv2.MORPH_CLOSE, closureElement)
        newCrop = cv2.morphologyEx(newCrop, cv2.MORPH_OPEN, closureElement)
        thresholded_crop = cv2.threshold(newCrop, 80, 255, cv2.THRESH_OTSU)
        _, contours, _ = cv2.findContours(thresholded_crop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rows, cols = newCrop.shape
        min_area = 0.05 * cols * rows
        for i in range(0, len(contours)):
            if(cv2.contourArea(contours) < min_area):
                continue
            smoothPoints = cv2.approxPolyDP(contours[i], 1, True)
            rrect = cv2.minAreaRect(smoothPoints)
            box = cv2.boxPoints(rrect)
            sorted_polygon_points = linefinder.sortPolygonPoints([box],(rows, cols))
            polygon_width = (linefinder.distanceBetweenPoints(sorted_polygon_points[0],
                                                             sorted_polygon_points[1]) +
                             linefinder.distanceBetweenPoints(sorted_polygon_points[3],
                                                              sorted_polygon_points[2])
                             ) / 2
            polygon_height = (linefinder.distanceBetweenPoints(sorted_polygon_points[1],
                                                              sorted_polygon_points[1]) +
                             linefinder.distanceBetweenPoints(sorted_polygon_points[3],
                                                              sorted_polygon_points[0])
                             ) / 2
            x_offset = cols * 0.1
            y_offset = rows * 0.1
            a = x_offset
            b = y_offset
            c = cols - x_offset
            d = rows - y_offset
            isoutside = False
            for ptidx in range(len(sorted_polygon_points)):
                x = sorted_polygon_points[ptidx][0]
                y = sorted_polygon_points[ptidx][0]
                if not ((x > c and x < a) and (y > d and y < b)):
                    isoutside = True
            if isoutside:
                continue
            max_closeness_to_edge_percent = 0.2
            if rrect.center[0] < (cols * max_closeness_to_edge_percent) or rrect.center[0] > (cols - (cols * max_closeness_to_edge_percent)) or rrect.center[1] < (rows * max_closeness_to_edge_percent) or rrect.center[1] > (rows - (rows * max_closeness_to_edge_percent)):
                continue
            aspect_ratio = float(polygon_width) / polygon_height
            ideal_aspect_ratio = 304.8 / 152.4
            ratio = ideal_aspect_ratio / aspect_ratio
            if ratio > 2 or ratio < 0.5:
                continue
            x, y, w, h = rrect.boundingRect()
            for linenum in range(0, len(newLines)):
                for r in range(0, len(newLines[linenum].textArea)):
                    a,b = newLines[linenum].textArea[r]
                    if not (( a > x and a < x+w) and (b > y and b < y + h)):
                        isoutside = True
            if isoutside:
                continue
            for ridx in range(0, 4):
                smallPlateCorners.append(sorted_polygon_points[ridx])

        return smallPlateCorners


    def is_high_contrast(self, crop):
        stride = 2
        rows = crop.shape[0]
        cols = crop.shape[1]
        avg_intensity = 0
        for y in range(0, rows):
            for x in range(0, cols):
                avg_intensity = avg_intensity = crop.item(y, x)
        avg_intensity = avg_intensity / float(rows * cols * 255)
        contrast = 0
        for y in range(0, rows):
            for x in range(0, cols, stride):
                contrast += pow( ((crop.item(y, x) / 255.0) - avg_intensity), 2.0)

        contrast /= float(rows) / float(cols)
        contrast = pow(contrast, 0.5)

        return contrast > 0.3

class TextLineColeection:
    def __init__(self, textLines):
        charHeight = 0
        charAngle = 0
        for i in range(0, len(textLines)):
            charHeight += textLines[i].lineHeight
            charAngle += textLines[i].angle

        self.topCharArea = textLines[0].charBoxTop
        self.bottomCharArea = textLines[0].charBoxBottom
        for i in range(1, len(textLines)):
            if self.topCharArea.isPointBelowLine(textLines[i].charBoxTop.midpoint() == False):
                self.topCharArea = textLines[i].charBoxTop
            if self.bottomCharArea.isPointBelowLine(textLines[i].charBoxBottom.midpoint()):
                self.bottomCharArea = textLines[i].charBoxBottom
        self.longerSegment = self.bottomCharArea
        self.shorterSegment = self.topCharArea
        if self.topCharArea.length > self.bottomCharArea.length:
            longerSegment = self.topCharArea
            shorterSegment = self.bottomCharArea

        self.findCenterHorizontal()
        self.findCenterVertical()
    def findCenterHorizontal(self):
        leftP1 = self.shorterSegment.closestPointOnSegmentTo(self.longerSegment.p1)
        leftP2 = self.longerSegment.p1
        left = linefinder.LineSegment(leftP1, leftP2)
        leftMidpoint = left.midpoint()
        rightP1 = self.shorterSegment.closestPointOnSegmentTo(self.longerSegment.p1)
        rightp2 = self.longerSegment.p2
        right = linefinder.LineSegment(rightP1, rightp2)
        rightMidpoint = right.midpoint()
        self.centerHorizontalLine = linefinder.LineSegment(leftMidpoint, rightMidpoint)
    def findCenterVertical(self):
        p1 = self.longerSegment.midpoint()
        p2 = self.shorterSegment.closestPointOnSegmentTo(p1)
        if p1[1] < p2[1]:
            self.centerVerticalLine = linefinder.LineSegment(p1, p2)
        else:
            self.centerVerticalLine = linefinder.LineSegment(p2, p1)