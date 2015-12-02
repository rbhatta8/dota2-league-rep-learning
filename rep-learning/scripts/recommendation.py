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
from sklearn.cross_decomposition import PLSRegression
import operator
import os

SEGMENT_STATS = ['kills', 'deaths', 'assists', 'wards', 'towers', 'inhibitors',
                 'gold', 'level', 'jungle_cs', 'cs', 'damage_taken', 'barons',
                 'blues', 'reds', 'dragons', 'heralds']

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
                        help='Path and prefix for files containing training data')

    parser.add_argument('-Y', '--Y-labels',
                        type=str, required=True,
                        help='Path to file containing labels for original training data')

    parser.add_argument('-M', '--match-data',
                        type=str, required=True,
                        help='Path to file containing match data of the player')

    parser.add_argument('-P', '--projection',
                        type=str, required=True,
                        help='Path to file containing projection space for the data')

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
    

def clusters_to_indices(cluster_labels):
    '''
    Convenience function to form
    a dictionary that maps cluster labels
    to indices in the original data that
    belong to those clusters

    Params:
    -------
    cluster_labels : list
        contains cluster label assignments for each training data point
    in the original data

    Returns:
    --------
    clusters_to_inds : dict
        cluster labels as keys mapped to list of indices with that label as values
    '''

    unique_clusters = set(cluster_labels)
    clusters_to_inds = {c:[] for c in unique_clusters}

    for i in range(len(cluster_labels)):
        cluster_label = cluster_labels[i]
        clusters_to_inds[cluster_label].append(i)
    
    return clusters_to_inds
    
def predict_cluster_labels(clustering_obj, new_data):
    '''
    Predict cluster labels for new data

    Params:
    -------
    clustering_obj : sklearn obj
        object that was produced after clustering training data

    new_data : 2d np array
        new data whose cluster labels are to be predicted

    Returns:
    --------
    predicted_cluster_labels : list
        list containing the predicted cluster labels
    '''

    predicted_cluster_labels = clustering_obj.predict(new_data)
    return predicted_cluster_labels

def get_sorted_label_occurrences(labels):
    '''
    Get a sorted list of labels occurring in
    descending order of their frequency

    Params:
    ------
    labels : list
       list of the labels

    Returns:
    --------
    sorted_labels_occurrence : list of tuples
        list of (label, frequency)
    '''

    # count occurrences for each cluster
    unique_labels = set(labels)
    labels_occurrence_dict = dict(zip(unique_labels, [0]*len(unique_labels)))
    for c in labels:
        labels_occurrence_dict[c] += 1

    # sort by frequency of occurrence
    # in descending order note this a list of tuples
    # with (label, n_occurrences)
    sorted_labels_occurrence = sorted(labels_occurrence_dict.items(), key=operator.itemgetter(1))
    sorted_labels_occurrence.reverse()

    return sorted_labels_occurrence
    
def recommend_pls_strategy(player_data, train_data, projection, clustering_obj):

    ''' 
    Recommends a ranking of champions a player should play
    based on the players' match data provided and previously
    clustered training data

    Parameters:
    ----------

    player_data : 2d numpy array
        match data of the player

    train_data  : 2d numpy array
        the original training data

    projection  : 2d numpy array
        projection matrix generated from a manifold learning technique

    clustering_obj : sklearn object
        an object that contains clustering information of the training data

    train_labels : list
        list of training labels that the recommendations will be based on

    Returns:
    --------

    None : simply displays the recommendation
    '''
    
    # first project the data into the correct space
    projected_player_data = np.dot(player_data, np.transpose(projection))
    
    # get the cluster labels on the training data
    train_clusters = clustering_obj.labels_

    # assign clusters to each match we have of the player
    player_match_clusters = predict_cluster_labels(clustering_obj, projected_player_data)

    # get cluster to index mapping for training matches
    training_matches_cluster_indices = clusters_to_indices(train_clusters)


def visualize_s0_regression(s0_predictor, rs, s0):
    # s0_predictor is a PLSRegression predictor object; rs is an entry from the X matrix input to the predictor; s0 is corresponding Y entry
    s0_hat = np.round(s0_predictor.predict(rs), 0)
    err = np.round(abs(s0 - s0_hat)/(s0+1)*100, 0)
    out_str = ""
    for i in range(len(SEGMENT_STATS)):
        out_str += "{0}: {1} ({2}) [{3}% error]\n".format(SEGMENT_STATS[i], s0_hat[i], s0[i], err[i])
    return out_str

def visualize_s1_regression(s1_predictor, s0, s1):
    # s1_predictor is a PLSRegression predictor object; s0 is an entry from the X matrix input to the predictor; s1 is corresponding Y entry
    s1_hat = np.round(s1_predictor.predict(s0), 0)
    err = np.round(abs(s1 - s1_hat)/(s1+1)*100, 0)
    out_str = ""
    for i in range(len(SEGMENT_STATS)):
        out_str += "{0}: {3} --> {2} ({1}) [{4}% error]\n".format(SEGMENT_STATS[i], s1[i], s1_hat[i], s0[i], err[i])
    return out_str


def recommend_champions_ranking(player_data, train_data_end, train_data_s0, train_data_s1, projection, clustering_obj, train_labels):
    ''' 
    Recommends a ranking of champions a player should play
    based on the players' match data provided and previously
    clustered training data

    Parameters:
    ----------

    player_data : 2d numpy array
        match data of the player

    projection  : 2d numpy array
        projection matrix generated from a manifold learning technique

    clustering_obj : sklearn object
        an object that contains clustering information of the training data

    train_labels : list
        list of training labels that the recommendations will be based on

    Returns:
    --------

    None : simply displays the recommendation
    '''

    # first project the data into the correct space
    projected_player_data = np.dot(player_data, np.transpose(projection))

    # get the cluster labels on the training data
    train_clusters = clustering_obj.labels_

    # assign clusters to each match we have of the player
    player_match_clusters = predict_cluster_labels(clustering_obj, projected_player_data)

    # get a sorted list (descending order) of clusters and frequency of occurrence
    sorted_cluster_occurrence = get_sorted_label_occurrences(player_match_clusters)

    # get most frequent cluster
    most_freq_cluster = sorted_cluster_occurrence[0][0]
    print "Most frequent cluster", most_freq_cluster

    associated_train_labels = [train_labels[i] for i in range(len(train_labels)) if train_clusters[i] == most_freq_cluster]

    # get a sorted list (descending order) of training labels and frequency of occurrence
    sorted_label_occurrence = get_sorted_label_occurrences(associated_train_labels)

    # display in order of frequency as a recommendations for the player
    print "Rankings for recommended champions to play"
    for item in sorted_label_occurrence:
        print item[0], item[1]

    # get cluster to index mapping for training matches
    training_matches_cluster_indices = clusters_to_indices(train_clusters)

    # get indices for the most frequent cluster
    match_indices_most_freq_cluster = training_matches_cluster_indices[most_freq_cluster]
    
    # form the matrices for regression
    regress_end_stats = train_data_end[match_indices_most_freq_cluster]
    regress_s0 = train_data_s0[match_indices_most_freq_cluster]
    regress_s1 = train_data_s1[match_indices_most_freq_cluster]

    # fit PLSRegress predictors for s0 and s1
    PLS_s0 = PLSRegression(n_components = 3)
    PLS_s1 = PLSRegression(n_components = 3)
    s0_predictor = PLS_s0.fit(regress_end_stats, regress_s0)
    s1_predictor = PLS_s1.fit(regress_s0, regress_s1)

    # for visualization of regression, choose [0-th] match instance from cluster
    rs = regress_end_stats[0, :]
    s0 = regress_s0[0, :]
    s1 = regress_s1[0, :]

    # visualize
    print "s0 Prediction"
    print visualize_s0_regression(s0_predictor, rs, s0)
    print "s1 Prediction"
    print visualize_s1_regression(s1_predictor, s0, s1)

    
                        

def main():

    # get the required arguements from
    # the user
    opts = parse_arguements()
    train_path = opts['train_data']
    labels_path = opts['Y_labels']
    player_matches_path = opts['match_data']
    clustering_path = opts['clustering']
    projection_path = opts['projection']
    output_name = opts['output']
    pickle_name = opts['output_pickle']

    # load the pickles
    train_data_end = pickle.load(open(train_path + "_relevant_stats_winners", 'rb'))
    train_data_s0 = pickle.load(open(train_path + "_segment_0_stats_winners", 'rb'))
    train_data_s1 = pickle.load(open(train_path + "_segment_1_stats_winners", 'rb'))
    train_labels = pickle.load(open(labels_path, 'rb'))
    player_data = pickle.load(open(player_matches_path, 'rb'))
    clustering = pickle.load(open(clustering_path, 'rb'))
    projection = pickle.load(open(projection_path, 'rb'))

    recommend_champions_ranking(player_data, train_data_end, train_data_s0, train_data_s1, projection, clustering, train_labels)
    #recommend_pls_strategy(player_data, train_data, projection, clustering)

main()

