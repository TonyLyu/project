from lbp import LocalBinaryPattern
from sklearn.svm import LinearSVC
from imutils import paths
import  argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-t","--training", required=Ture, help="path  to the training images")
ap.add_argument("-e","--testing", required=Ture, help="path to the testing images")
args = vars(ap.parse_args())
desc = LocalBinaryPattern(24,8)
data = []
labels = []
#loop over the training images
for imagePath in paths.list_images(args["trainging"]):
	#load the image
	image = cv2.imread(imagePath)
	#convert it to grayscale and describe it
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	hist = desc.describe(gray)

	labels.append(imagePath.split("/")[-2])
	data.append(hist)

#train a linear SVM on the data
model = LinearSVC(C=100.0, random_state=42)
model.fit(data, labels)


