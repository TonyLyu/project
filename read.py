import numpy as np
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest, chi2, f_classif
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.multiclass import OutputCodeClassifier
from sklearn.multiclass import OneVsRestClassifier
subtypes = ['Basal', 'Her2', 'LumA', 'LumB', 'Normal']
csv = np.genfromtxt('Breastcancer.csv', delimiter=",", dtype=None)
lambels = csv[1:, -1:]
features = np.array(csv[0:1, :-1])[0]
print(features)
lambels = np.array(lambels).transpose()[0]
data = csv[1:, :-1]
X = np.array(data, dtype=float)
y = [subtypes.index(x) if x in subtypes else 0 for x in lambels]

# min_max_scaler = preprocessing.MinMaxScaler()
# X = min_max_scaler.fit_transform(X)

ch2 = SelectKBest(f_classif, k=40)
X = ch2.fit_transform(X, y)
a = []
result = ch2.get_support()
for i in xrange(len(result)):
    if result[i]:
        a.append(features[i])
print(a)
# print(ch2.scores_[0])
classif = OneVsRestClassifier(LDA(solver='svd'))
#classif = OutputCodeClassifier(LDA(solver='svd'))
classif.fit(X, y)

print(classif.score(X, y))
#clf1 = LDA(solver='svd', shrinkage=None).fit(X, y)
# result_label = clf1.predict(X)
# score = clf1.score(X, y)
# y_pred = qda.fit(X, y).predict(X)
# count = 0
# for i in range(len(y_pred)-1):
#     if y_pred[i] == y[i]:
#         count += 1

# print(float(count/len(y_pred)))

