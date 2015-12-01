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

    parser.add_argument('-op', '--output-pickle',
                        type=str, required=True,
                        help='Path, including name of the output pickle for the PCA representation')

    parser.add_argument('-nc', '--num-components',
                        type=int, default=2,
                        help='Num components to compute representation for')

    args = parser.parse_args()
    opts = vars(args)
    return opts
    

# get the required arguements from
# the user
opts = parse_arguements()
X_path = opts['X_data']
Y_path = opts['Y_labels']
output_name = opts['output']
pickle_name = opts['output_pickle']
arg_components = opts['num_components']

# load the pickles, load Y only if given
X = pickle.load(open(X_path, 'rb'))

if Y_path:
    Y = pickle.load(open(Y_path, 'rb'))

n_samples, n_features = X.shape

# Computing PCA representation
print("Computing PCA representation")
pca = decomposition.PCA(arg_components, whiten=True)
X_pca = pca.fit(X).transform(X)

# if we are given labels use them, otherwise initialize all
# to be the same
if Y_path:
    labels = Y
else:
    labels = [0]*n_samples

# do 2d visualization or 3d
if arg_components == 2:                                                                 
    visualization.visualize2d(X_pca, labels, output_name)

elif arg_components == 3:
    visualization.visualize3d(X_pca, labels, output_name)


# save the PCA representation as a pickle
pickle.dump(X_pca, open(pickle_name, 'wb'))
