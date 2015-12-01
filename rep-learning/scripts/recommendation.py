"""
Script to make player-specific recommendations

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
    parser.add_argument('-T', '--train-data',
                        type=str, required=True,
                        help='Path to file containing original training data')

    parser.add_argument('-Y', '--Y-labels',
                        type=str, required=True,
                        help='Path to file containing labels for original training data')

    parser.add_argument('-M', '--match-data',
                        type=str, required=True,
                        help='Path to file containing match data of the player')

    parser.add_argument('-C', '--clustering',
                        type=str, required=True,
                        help='Path to file containing affinity propagation clustering on training data')

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
train_path = opts['train_data']
labels_path = opts['Y_labels']
player_matches_path = opts['match_data']
clustering_path = opts['clustering']
output_name = opts['output']
pickle_name = opts['output_pickle']

# load the pickles, load Y only if given
train_data = pickle.load(open(train_data, 'rb'))
train_labels = pickle.load(open(labels_path, 'rb'))
player_data = pickle.load(open(labels_path, 'rb'))
clustering = pick.load(open(clustering_path, 'rb'))

# assign clusters to each match we have of the player
player_match_labels = clustering.fit_predict(player_data)

print player_match_labels

