"""
Script to perform LLE

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
import sys
import argparse

def parse_arguements():
    """
    Function to parse command line
    arguements from the user

    Returns
    ------
    opts : dict
        command line arguements from the user
    """

    info = "Perform LLE on a given X matrix of data and optional Y labels"
    parser = argparse.ArgumentParser(description=info)

    # program arguments
    parser.add_argument('-X', '--X-data',
                        type=str, required=True,
                        help='Path to file containing X data')

    parser.add_argument('-Y', '--Y-labels',
                        type=str, default=None,
                        help='Path to file containing Y labels (optional)')

    parser.add_argument('-o', '--output',
                       type=str, required=True,
                       help='Path, including name of the output png')

    parser.add_argument('-nn', '--num-neighbours',
                         type=int, default=10,
                         help='Num neighbors to use for the LLE')

    parser.add_argument('-nc', '--num-components',
                         type=int, default=2,
                         help='Num components to use for the LLE representation')

    args = parser.parse_args()
    opts = vars(args)
    return opts
    

# get the required arguements from
# the user
opts = parse_arguements()
X_path = opts['X_data']
Y_path = opts['Y_labels']
output_name = opts['output']
n_neighbors = opts['num_neighbours']
arg_components = opts['num_components']

# load the pickles, load Y only if given
X = pickle.load(open(X_path, 'rb'))

if Y_path:
    Y = pickle.load(open(Y_path, 'rb'))

n_samples, n_features = X.shape

# Locally linear embedding of the dataset
print("Computing LLE embedding")
clf = manifold.LocallyLinearEmbedding(n_neighbors, n_components=arg_components,
                                      method='standard')
t0 = time()
X_lle = clf.fit_transform(X)
print("Done. Reconstruction error: %g" % clf.reconstruction_error_)

# plot the raw data
plt.scatter(X_lle[:, 0], X_lle[:, 1])

# plot the labels only if given
if Y_path:

    # make a colour map that colours the points
    # based on their unique labels
    unique_labels = set(Y)
    num_unique_labels = len(unique_labels)
    unique_labels_dict = dict(zip(unique_labels, range(num_unique_labels))) 
    colour_map = [unique_labels_dict[l] for l in unique_labels_dict]
    
    # plot using this colour map
    plt.scatter(X_lle[:,0], X_lle[:,1], c=colour_map)

    '''
    for i in range(len(Y)):
        plt.text(X_lle[i, 0], X_lle[i, 1], Y[i], 
                 color=plt.cm.Set1(random.randint(1, 110)),
                 fontdict={'weight': 'bold', 'size': 4})
    '''

else:
    plt.scatter(X_lle[:, 0], X_lle[:, 1])

# save the figure
plt.savefig(output_name)
plt.show()
