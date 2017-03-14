import cv2
import numpy as np
import math
import linefinder

class PlateLines:
    def __init__(self, img_data):
        self.img_data = img_data

    def __init__(self):
        self = self
        self.line = None
        self.confidence = 0

    def preocessImage(self, inputImage, textLines, sensitivity):
        avgPixelIntensity = cv2.mean(inputImage)
        if avgPixelIntensity[0] >= 252:
            return
        elif avgPixelIntensity[0] <= 3:
            return
        smoothed = cv2.bilateralFilter(inputImage, 3, 45, 45)
        edges = cv2.Canny(smoothed, 66, 133)
        mask = np.zeros((inputImage.shape[0], inputImage.shape[1]), dtype="uint8")
        for i in range(0, len(textLines)):
            polygons = []
            polygons.append(textLines[i].textArea)
            cv2.fillPoly(mask, polygons, (255, 255, 255))
            mask = cv2.dilate(mask, cv2.getStructuringElement(1, (2, 3), (1, 1)))
            mask = cv2.bitwise_not(mask)
            edges = cv2.bitwise_and(edges, mask)
            hlines = self.getLines()
    def getLines(self, edges, sensitivityMultiplier, vertical):
        horizontal_sensitivity = 45
        vertical_sensitivity = 25
        filteredLines =[]
        if vertical:
            sensitivity = vertical_sensitivity * (1.0 / sensitivityMultiplier)
        else:
            sensitivity = horizontal_sensitivity * (1.0 / sensitivityMultiplier)
        allLines = cv2.HoughLines(edges, 1, math.pi/180, sensitivity, 0, 0)
        for i in range(0, len(allLines)):
            rho = allLines[i][0]
            theta = allLines[i][1]
            pt1 = pt2 = (0, 0)
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            angle = theta * (180 / math.pi)
            pt1[0] = round(x0 + 1000 * (-b))
            pt1[1] =round(y0 + 1000 * (a))
            pt2[0] = round(x0 - 1000 * (-b))
            pt2[1] = round(y0 - 1000 * (a))
            if vertical:
                if angle < 20 or angle > 340 or (angle > 160 and angle < 210):
                    if pt1[1] <= pt2[1]:
                        line = linefinder.LineSegment(pt2[0], pt2[1], pt1[0], pt1[1])
                    else:
                        line = linefinder.LineSegment(pt1[0], pt1[1], pt2[0], pt2[1])
                    top = linefinder.LineSegment(0, 0, edges.shape[1], 0)
                    bottom = (0, edges.shape[0], edges.shape[1], edges.shape[0])
                    p1 = line.intersection(bottom)
                    p2 = line.intersection(top)
                    plateLine = PlateLines()
                    plateLine.line = linefinder.LineSegment(p1[0], p1[1], p2[0], p2[1])
                    plateLine.confidence = (1.0 - 0.3) * (float(len(allLines) - i)) / float(len(allLines)) + 0.3
                    filteredLines.append(plateLine)
            else:
                if (angle > 70 and angle < 110) or (angle > 250 and angle < 290):
                    if pt1[0] <= pt2[0]:
                        line = linefinder.LineSegment(pt1[0], pt1[1], pt2[0], pt2[1])
                    else:
                        line = linefinder.LineSegment(pt2[0], pt2[1], pt1[0], pt1[1])
                    newY1 = line.getPointAt(0)
                    newY2 = line.getPointAt(edges.shape[1])
                    plateLine = PlateLines()
                    plateLine.line = linefinder.LineSegment(0, newY1, edges.shape[1], newY2)
                    plateLine.confidence = (1.0 - 0.3) * (float(len(allLines) - i)) / float(len(allLines)) + 0.3
                    filteredLines.append(plateLine)


        return filteredLines


