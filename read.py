import numpy as np 
from sklearn.feature_selection import SelectKBest, chi2
subclass=[''];
csv = np.genfromtxt('Breastcancer.csv', delimiter=",", dtype=None)
lambel = csv[1:, -1:]
lambel = np.array(lambel).transpose()
data = csv[1:, :-1]
data = np.array(data, dtype=float)
ch2 = SelectKBest(chi2, k=20)
result =
