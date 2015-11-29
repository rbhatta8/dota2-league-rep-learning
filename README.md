# dota2-league-rep-learning

# Perform LLE on league participant stats
python rep-learning/lle.py -X league/pickles/X_relevant_stats -o league/results/relevant_participant_stats_lle.png -nn 5

# Perform PCA on league participant stats
python rep-learning/pca.py -X league/pickles/X_relevant_stats -o league/results/relevant_participant_stats_pca.png -nc 2