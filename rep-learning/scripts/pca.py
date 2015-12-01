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
import argparse
from mpl_toolkits.mplot3d import Axes3D

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

# plot the labels only if given                                                                                                              

if Y_path:

    # make a colour map that colours the points                                                                                              
    # based on their unique labels
    unique_labels = set(Y)
    num_unique_labels = len(unique_labels)
    unique_labels_dict = dict(zip(unique_labels, range(num_unique_labels)))
    colour_map = [unique_labels_dict[l] for l in Y]

    # plot using this colour map                     

    '''
    for i in range(len(Y)):
        plt.text(X_lle[i, 0], X_lle[i, 1], Y[i],
                 color=plt.cm.Set1(random.randint(1, 110)),
                 fontdict={'weight': 'bold', 'size': 4})
    '''
else:
    colour_map = np.ones((n_samples, 1))


if arg_components == 2:                                                                 
    plt.scatter(X_pca[:,0], X_pca[:,1], c=colour_map)

else:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X_pca[:,0], X_pca[:,1], X_pca[:,2], c=colour_map)

# save the figure
plt.savefig(output_name)
plt.show()

# save the PCA representation as a pickle
pickle.dump(X_pca, open(pickle_name, 'wb'))