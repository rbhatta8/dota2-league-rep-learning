"""
Script to perform LLE

authors : Rohit Bhattacharya, Azwad Sabik
emails  : rohit.bhattachar@gmail.com, azwadsabik@gmail.com
"""

# imports
from time import time
from sklearn import decomposition
import pickle
import numpy as np
import matplotlib.pyplot as plt
import random
import sys

X_pickle = sys.argv[1]
Y_pickle = sys.argv[2]
output_name = sys.argv[3]

X = pickle.load(open(X_pickle, 'rb'))
Y = pickle.load(open(Y_pickle, 'rb'))

n_samples, n_features = X.shape

# pca of the dataset
print("Computing PCA representation")
n_components = 2
pca = decomposition.PCA(n_components)
X_pca = pca.fit(X).transform(X)

plt.scatter(X_pca[:, 0], X_pca[:, 1])
for i in range(len(Y)):
    plt.text(X_pca[i, 0], X_pca[i, 1], Y[i], 
            color=plt.cm.Set1(random.randint(1, 110)),
            fontdict={'weight': 'bold', 'size': 4})

plt.savefig('../results/' + output_name + '.png')
plt.show()
