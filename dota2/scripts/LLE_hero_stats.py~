# -*- coding: utf-8 -*-
"""
Script to perform LLE analysis on DOTA 2 characters' base statistics

authors : Rohit Bhattacharya, Azwad Sabik
emails  : rohit.bhattachar@gmail.com, azwadsabik@gmail.com
"""

# imports
from time import time
from sklearn import manifold
import pickle
import numpy as np
import matplotlib.pyplot as plt
import random

hero_stats = pickle.load(open('hero_stats.p', 'rb'))
X = np.zeros((0, len(hero_stats.values()[0][0:6])))
Y = []
for hero in hero_stats:
    X = np.vstack((X, np.array(hero_stats[hero][0:6])))
    Y.append(hero)
print hero_stats['Outworld_Devourer']

n_samples, n_features = X.shape
n_neighbors = 30

# Locally linear embedding of the dataset
print("Computing LLE embedding")
clf = manifold.LocallyLinearEmbedding(n_neighbors, n_components=2,
                                      method='standard')
t0 = time()
X_lle = clf.fit_transform(X)
print("Done. Reconstruction error: %g" % clf.reconstruction_error_)

plt.scatter(X_lle[:, 0], X_lle[:, 1])
for i in range(len(Y)):
    plt.text(X_lle[i, 0], X_lle[i, 1], Y[i], 
            color=plt.cm.Set1(random.randint(1, 110)),
            fontdict={'weight': 'bold', 'size': 6})

plt.savefig('dota_hero_LLE.png')
