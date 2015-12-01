"""
Script to give recommendations to players

authors : Rohit Bhattacharya, Azwad Sabik
emails  : rohit.bhattachar@gmail.com, azwadsabik@gmail.com
"""

# imports
import pickle
import numpy as np
import visualization
import argparse
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import AffinityPropagation

def parse_arguements():
    """
    Function to parse command line
    arguements from the user

    Returns
    ------
    opts : dict
        command line arguements from the user
    """

    info = "Perform affinity propagation on the given data"
    parser = argparse.ArgumentParser(description=info)

    # program arguments
    parser.add_argument('-X', '--train-data',
                        type=str, required=True,
                        help='Path to file containing original training data')

    parser.add_argument('-Y', '--Y-labels',
                        type=str, required=True,
                        help='Path to file containing labels for original training data')

    parser.add_argument('-M', '--match-data',
                        type=str, required=True,
                        help='Path to file containing match data of the player')

    parser.add_argument('-o', '--output',
                       type=str, required=True,
                       help='Path, including name of the output png')

    parser.add_argument('-op', '--output_pickle',
                        type=str, required=True,
                        help='Path, including name of the output pickle storing the AP representation')

    args = parser.parse_args()
    opts = vars(args)
    return opts
    

# get the required arguements from
# the user
opts = parse_arguements()
X_path = opts['X_data']
preference_param = opts['preference_param']
output_name = opts['output']
pickle_name = opts['output_pickle']

# load the pickles, load Y only if given
train_data = pickle.load(open(train_data, 'rb'))
Y = pickle.load(open(Y_path, 'rb'))

n_samples, n_features = X.shape



