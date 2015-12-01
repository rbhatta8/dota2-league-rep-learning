"""
Script to perform clustering via affinity propagation

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
from collections import Counter

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
    parser.add_argument('-X', '--X-data',
                        type=str, required=True,
                        help='Path to file containing X data')

    parser.add_argument('-Y', '--Y-labels',
                        type=str, default=None,
                        help='Path to file containing Y (true) labels (optional)')

    parser.add_argument('-p', '--preference-param',
                        type=float, default=-50,
                        help='Preference parameter used in affinity propagation')

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
Y_path = opts['Y_labels']
preference_param = opts['preference_param']
output_name = opts['output']
pickle_name = opts['output_pickle']

# load the pickles, load Y only if given
X = pickle.load(open(X_path, 'rb'))

if Y_path:
    Y = pickle.load(open(Y_path, 'rb'))

n_samples, n_features = X.shape


# Computing affinity propagation clustering
print("Clustering using affinity propagation")
af = AffinityPropagation(preference=preference_param, max_iter=1000).fit(X)

# display clustering statistics
labels = af.labels_
print labels
print ('Counts for each label')
label_counts = Counter(labels).values()
n_clusters = len(set(labels))
print ('Estimated number of clusters: %d' %n_clusters)

# filter out clusters that had only 1 member as possible outliers
label_signif_counts = [c for c in label_counts if c > 1]
n_signif_clusters = len(label_signif_counts)
print ('Counts for each "significant" label')
print label_signif_counts
print ('Estimated number of "significant" clusters: %d' %n_signif_clusters)

# save the 
if n_features == 2:
    visualization.visualize2d(X, labels, output_name)

elif n_features ==3:
    visualization.visualize3d(X, labels, output_name)

# save the affinity propagation representation as a pickle
pickle.dump(af, open(pickle_name, 'wb'))
