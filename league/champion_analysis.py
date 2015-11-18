# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 08:50:08 2015

@author: Azwad
"""

from riotwatcher import RiotWatcher
import pickle
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn import manifold
from sklearn import decomposition

with open('Veraxios_API_Key.txt', 'r') as f:
     lol = RiotWatcher(f.read().strip())
     
class Champion:
    def __init__(self, identifier):
        self.data = lol.static_get_champion(identifier, champ_data='stats')
        self.data.update(lol.static_get_champion(identifier, champ_data='tags'))
        self.stats = self.data['stats']
        self.tags = self.data['tags']
        self.name = str(self.data['name'])
    def stats_vector(self):
        vec = np.zeros((1, len(self.stats)))
        stats_keys = self.stats.keys() 
        for i in range(len(self.stats)):
            vec[0, i] = self.stats[stats_keys[i]]
        return vec        
     
def get_champions(ids = None):
    champions = []
    if ids == None:
        ids = []
        static_champ_list_data = lol.static_get_champion_list()['data']
        for champ_data in static_champ_list_data.values():
            ids.append(champ_data['id'])
    for identifier in ids:
        champions.append(Champion(identifier))
        print champions[-1].name
    return champions

def get_champion_datapoints(champions):
    X = np.zeros((0, 20))
    names = []
    tags = []
    for champion in champions:
        X = np.vstack((X, champion.stats_vector()))
        names.append(champion.name)
        tags.append(str(champion.tags[0]))
    return X, names, tags
        
# champions = get_champions()

# with open('champions.p', 'w') as c:
#    champions = pickle.dump(champions, c)        
        
with open('champions.p', 'r') as c:
    champions = pickle.load(c)

X, names, tags = get_champion_datapoints(champions)
n_samples, n_features = X.shape

# Locally linear embedding of the dataset
print("Computing LLE embedding")
n_neighbors = 30
clf = manifold.LocallyLinearEmbedding(n_neighbors, n_components=2,
                                      method='standard')                                     
X_lle = clf.fit_transform(X)
print("Done. Reconstruction error: %g" % clf.reconstruction_error_)

# PCA
print("Computing PCA representation")
n_components = 2
pca = decomposition.PCA(n_components)
X_pca = pca.fit(X).transform(X)

#Visualize
colors = random.sample(range(n_samples), n_samples)

tag_colors = {}
tag_color = 0
for tag in tags:
    if tag not in tag_colors:
        tag_colors[tag] = tag_color
        tag_color += 15
        
#plt.subplot('111')
#plt.scatter(X_lle[:, 0], X_lle[:, 1])
#for i in range(len(names)):
#    plt.text(X_lle[i, 0], X_lle[i, 1], names[i], 
#            color=plt.cm.Set1(colors[i]),
#            fontdict={'weight': 'bold', 'size': 6})
            
plt.subplot('121')
plt.title('LLE')
plt.scatter(X_lle[:, 0], X_lle[:, 1])
for i in range(len(names)):
    plt.text(X_lle[i, 0], X_lle[i, 1], names[i], 
            color=plt.cm.Set1(tag_colors[tags[i]]),
            fontdict={'weight': 'bold', 'size': 6})
            
plt.subplot('122')
plt.title('PCA')
plt.scatter(X_pca[:, 0], X_pca[:, 1])
for i in range(len(names)):
    plt.text(X_pca[i, 0], X_pca[i, 1], names[i], 
            color=plt.cm.Set1(tag_colors[tags[i]]),
            fontdict={'weight': 'bold', 'size': 6})
plt.show()
