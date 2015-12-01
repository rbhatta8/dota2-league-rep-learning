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
import operator

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
train_data = pickle.load(open(train_path, 'rb'))
train_labels = pickle.load(open(labels_path, 'rb'))
player_data = pickle.load(open(player_matches_path, 'rb'))
clustering = pickle.load(open(clustering_path, 'rb'))

# assign clusters to each match we have of the player
player_match_clusters = clustering.predict(player_data)

# count occurrences for each cluster
unique_clusters = set(player_match_clusters)
cluster_occurrence_dict = dict(zip(unique_clusters, [0]*len(unique_clusters)))
for c in player_match_clusters:
    cluster_occurrence_dict[c] += 1

# sort by frequency of occurrence
# in descending order note this a list of tuples
# with (cluster, n_occurrences)
sorted_cluster_occurrence = sorted(cluster_occurrence_dict.items(), key=operator.itemgetter(1))
sorted_cluster_occurrence.reverse()

# get most frequent cluster
most_freq_cluster = sorted_cluster_occurrence[0][0]

# get training labels belonging to that cluster
# in the training data
train_clusters = clustering.labels_
associated_train_labels = [train_labels[i] for i in range(len(train_clusters)) if train_clusters[i] == most_freq_cluster]

# do a ranking of these labels by occurrence
unique_labels = set(associated_train_labels)
label_occurrence_dict = dict(zip(unique_labels, [0]*len(unique_labels)))
for l in associated_train_labels:
    label_occurrence_dict[l] += 1
sorted_label_occurrence = sorted(label_occurrence_dict.items(), key=operator.itemgetter(1))
sorted_label_occurrence.reverse()

print "Rankings for recommended champions to play"
for item in sorted_label_occurrence:
    print item[0], item[1]
