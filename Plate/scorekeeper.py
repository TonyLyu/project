import cv2

class ScoreKeeper:
    def__init__(self):
        self.weight_ids = []
        self.weights = []
        self.scores = []
    def setScore(self, weight_id, score, weight):
        self.weight_ids.append(weight_id)
        self.scores.append(score)
        self.weighs.append(weight)
    def getTotal(self):
        score = 0
        for i in range(0, len(self.weights)):
            score += score[i] + weights[i]
        return score
    def size(self)
        return len(weight_ids)
