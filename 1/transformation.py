import cv2
import linefinder
class Transformation:
    def __init__(self, bigImage, smallImage, x, y, width, height):
        self.bigImage = bigImage
        self.smallImage = smallImage
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def transformSmallPointsTOBigImage(self, points):
        bigPoints = []
        for i in range(0, len(points)):
            bigX = points[i][0] * (float(self.width) / self.smallImage.shape[1])
            bigY = points[i][1] * (float(self.height) / self.smallImage.shape[0])

            bigX = bigX + self.x
            bigY = bigY + self.y

            bigPoints.append((bigX, bigY))
        return bigPoints

    def getTransformationMatrix(self, corners, width, height):
        quad_pts = []
        quad_pts.append((0, 0))
        quad_pts.append((width, 0))
        quad_pts.append((width, height))
        quad_pts.append((0, height))

        return self.getTransformationMatrix(corners, quad_pts)

    def getTransformationMatrix(self, corners, outputCorners):
        transmtx = cv2.getPerspectiveTransform(corners, outputCorners)
        return transmtx

    def getCropSize(self, areaCorners, targetSize):
        leftEdge = linefinder.LineSegment(round(areaCorners[3][0]), round(areaCorners[3][1]),
                                          round(areaCorners[0][0]), round(areaCorners[0][1]))
        rightEdge = linefinder.LineSegment(round(areaCorners[2][0]), round(areaCorners[2][1]),
                                          round(areaCorners[1][0]), round(areaCorners[1][1]))
        topEdge = linefinder.LineSegment(round(areaCorners[0][0]), round(areaCorners[0][1]),
                                          round(areaCorners[1][0]), round(areaCorners[1][1]))
        bottomEdge = linefinder.LineSegment(round(areaCorners[3][0]), round(areaCorners[3][1]),
                                          round(areaCorners[2][0]), round(areaCorners[2][1]))
    def crop(self, outputImageSize, transformationMatrix):
        deskewed = cv2.warpPerspective(self.bigImage, transformationMatrix,
                                       outputImageSize, cv2.INTER_CUBIC)
        return deskewed

    def remapSmallPointstoCrop(self, smallPoints, transformationMatrix):
        remappedPoints = cv2.perspectiveTransform(smallPoints, transformationMatrix)
        return remappedPoints