# dota2-league-rep-learning

# Perform the clustering pipeline for 2d pca
clusteringPCA2d:
	python rep-learning/scripts/pca.py -X league/pickles/X_relevant_stats_winners -o league/results/relevant_participant_stats_tags_coloured_winners_pca.png -nc 2 -Y league/pickles/tags_winners -op rep-learning/pickles/PCA_relevant_stats_winners_2d
	python rep-learning/scripts/affinity_propagation.py -X rep-learning/pickles/PCA_relevant_stats_winners_2d -o league/results/clustering_2d_pca.png -p -50 -op rep-learning/pickles/AP_PCA_2d

# Perform the clustering pipeline for 3d pca
clusteringPCA3d:
	python rep-learning/scripts/pca.py -X league/pickles/X_relevant_stats_winners -o league/results/relevant_participant_stats_tags_coloured_winners_pca.png -nc 3 -Y league/pickles/tags_winners -op rep-learning/pickles/PCA_relevant_stats_winners_3d
	python rep-learning/scripts/affinity_propagation.py -X rep-learning/pickles/PCA_relevant_stats_winners_3d -o league/results/clustering_3d_pca.png -p -50 -op ../../Desktop/AP_PCA_3d

# Perform the clustering pipeline for raw data
clusteringRaw:
	python rep-learning/scripts/affinity_propagation.py -X league/pickles/X_relevant_stats_winners -o league/results/clustering_raw.png -p -50

# Perform the clustering pipeline for 2d LLE
clusteringLLE2d:
	python rep-learning/scripts/lle.py -X league/pickles/X_relevant_stats_winners -o league/results/relevant_participant_stats_role_tag_winners_lle.png -nn 30 -Y league/pickles/tags_winners -op rep-learning/pickles/LLE_relevant_stats_winners_2d -nc 2
	python rep-learning/scripts/affinity_propagation.py -X rep-learning/pickles/LLE_relevant_stats_winners_2d -o league/results/clustering_lle.png -p -50 -op rep-learning/pickles/AP_LLE_2d

# Perform the clustering pipeline for 3d LLE
clusteringLLE3d:
	python rep-learning/scripts/lle.py -X league/pickles/X_relevant_stats_winners -o league/results/relevant_participant_stats_role_tag_winners_lle.png -nn 30 -Y league/pickles/tags_winners -op rep-learning/pickles/LLE_relevant_stats_winners_3d -nc 3
	python rep-learning/scripts/affinity_propagation.py -X rep-learning/pickles/LLE_relevant_stats_winners_3d -o league/results/clustering_lle.png -p -50 -op rep-learning/pickles/AP_LLE_3d

# perform PCA on a single players data
singlePlayerPCA:
	python rep-learning/scripts/pca.py -X league/pickles/M_relevant_stats -o league/results/single_player_stats_tags_coloured_winners_pca.png -nc 3 -op rep-learning/pickles/PCA_single_player_stats_3d

recommendationSystem:
# then proceed with the recommendations
	python rep-learning/scripts/recommendation.py -T league/pickles/X_relevant_stats_winners -Y league/pickles/tags_winners -M rep-learning/pickles/PCA_single_player_stats_3d -C ../../Desktop/AP_PCA_3d -o league/results/whatever -op league/pickles/whatever

# Windows
#python rep-learning\lle.py -X league\pickles\X_relevant_stats -o league\results\relevant_participant_stats_win_couloured_lle.png -nn 30 -Y league\pickles\wins