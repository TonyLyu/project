import cv2




class textcontours:
    def __init__(self, threshold, img):
        rows, cols = threshold.shape[:2]
        self.img = img
        self.weight = cols
        self.height = rows
        self.threshhold = threshold

    def getTextcontours(self):
        img2, self.contours, self.hierarchy = cv2.findContours(self.threshgold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(0, len(self.contours)):
            self.goodIndices.append(True)
        drawContours(self)
        return self

    def drawContours(self):
        img = cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGB)
        cv2.drawContours(img, self.contours, -1, (0, 255, 0), 1)
        cv2.imshow("contours", img)

    def getGoodIndicesCount(self):
        count = 0
        for i in range(0, len(self.goodIndices)):
            if self.goodIndices[i]:
                count += 1
        return count

    def getIndicesCopy(self):
        copyArray = []
        for i in range(0, len(goodIndices)):
            val = goodIndices[i]
            copyArray.append(val)
        return copyArray

    def setIndices(self, newIndices):
        if(len(newIndices) == len(self.goodIndices)):
            for i in range(0, len(newIndices)):
                self.goodIndices[i] = newIndices[i]
        else:
            print("error")



weight = 0
height = 0
goodIndices = []
def getTextContours(threshold):
    img2, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rows, cols = threshold.shape[:2]
    weight = cols
    height = rows
    return contours
def drawContours(img, contours):
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    cv2.drawContours(img, contours, -1, (0,255,0), 1)
    cv2.imshow("123", img)
def filter(img):
    rows, cols = img.shape[:2]
    starting_min_height = round(rows * 0.3)
    starting_max_height = round(rows * (0.3 + 0.2))
    height_step = round(rows * 0.1)
    num_steps = 4
    bestFitScore = -1
    # for i in range(0, num_steps):
    #     for z in range