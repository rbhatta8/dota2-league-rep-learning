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
import random
import sys
import argparse
import visualization

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

    parser.add_argument('-op', '--output-pickle',
                        type=str, required=True,
                        help='Path, including name of the output pickle for the PCA representation')

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
pickle_name = opts['output_pickle']

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

# if we are given labels use them, otherwise initialize all                                                                                           
# to be the same
if Y_path:
    labels = Y
else:
    labels = np.ones((n_samples, 1))

# do 2d visualization or 3d
if arg_components == 2:
    visualization.visualize2d(X_lle, labels, output_name)

elif arg_components == 3:
    visualization.visualize3d(X_lle, labels, output_name)

# save the LLE representation as a pickle
pickle.dump(X_lle, open(pickle_name, 'wb'))
