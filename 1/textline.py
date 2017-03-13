import cv2

class TextLine:
    def __init__(self, textArea, linePolygon, imgSize):
        textAreaInts = []
        linePolygonInts = []
        for i in range(0, len(textArea)):
            textAreaInts.append((round(textArea[i][0]), round(textArea[i][1])))
        for i in range(0, len(linePolygon)):
            linePolygonInts.append((round(linePolygon[i][0]), round(linePolygon[i][1])))
        self.initialize(textAreaInts, linePolygonInts, imgSize)
    def initialize(self, textArea, linePolygon, imgSize):

