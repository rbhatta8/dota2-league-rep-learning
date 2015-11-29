# dota2-league-rep-learning

# Perform LLE on league participant stats
python rep-learning/lle.py -X league/pickles/X_relevant_stats -o league/results/relevant_participant_stats_lle.png -nn 30

# Perform LLE on league participant stats w/ colour labelling
python rep-learning/lle.py -X league/pickles/X_relevant_stats -o league/results/relevant_participant_stats_lle_role_coloured.png -nn 30 -Y league/pickles/roles

# Perform LLE on league participant stats w/ colour labelling only for winners
python rep-learning/lle.py -X league/pickles/X_relevant_stats_winners -o league/results/relevant_participant_stats_role_coloured_winners_lle.png -nn 30 -Y league/pickles/roles_winners

# Perform PCA on league participant stats
python rep-learning/pca.py -X league/pickles/X_relevant_stats -o league/results/relevant_participant_stats_pca.png -nc 2