# dota2-league-rep-learning

# Perform the clustering pipeline for 2d pca
clusteringPipeline2d:
	python rep-learning/scripts/pca.py -X league/pickles/X_relevant_stats_winners -o league/results/relevant_participant_stats_tags_coloured_winners_pca.png -nc 2 -Y league/pickles/tags_winners -op rep-learning/pickles/PCA_relevant_stats_winners_2nc
	python rep-learning/scripts/affinity_propagation.py -X rep-learning/pickles/PCA_relevant_stats_winners_2nc -o league/results/clustering_2d_pca.png

# Perform the clustering pipeline for 3d pca
clusteringPipeline3d:
	python rep-learning/scripts/pca.py -X league/pickles/X_relevant_stats_winners -o league/results/relevant_participant_stats_tags_coloured_winners_pca.png -nc 3 -Y league/pickles/tags_winners -op rep-learning/pickles/PCA_relevant_stats_winners_3nc
	python rep-learning/scripts/affinity_propagation.py -X rep-learning/pickles/PCA_relevant_stats_winners_3nc -o league/results/clustering_3d_pca.png

# Perform the clustering pipeline for raw data
clusteringPipelineRaw:
	python rep-learning/scripts/affinity_propagation.py -X league/pickles/X_relevant_stats_winners -o league/results/clustering_raw.png
#
# Perform LLE on league participant stats w/ colour labelling
#python rep-learning/lle.py -X league/pickles/X_relevant_stats -o league/results/relevant_participant_stats_lle_role_coloured.png -nn 30 -Y league/pickles/roles

# Perform LLE on league participant stats w/ colour labelling only for winners
#python rep-learning/lle.py -X league/pickles/X_relevant_stats_winners -o league/results/relevant_participant_stats_role_coloured_winners_lle.png -nn 30 -Y league/pickles/roles_winners

# Windows
#python rep-learning\lle.py -X league\pickles\X_relevant_stats -o league\results\relevant_participant_stats_win_couloured_lle.png -nn 30 -Y league\pickles\wins

# Perform PCA on league participant stats
#python rep-learning/pca.py -X league/pickles/X_relevant_stats -o league/results/relevant_participant_stats_pca.png -nc 2

# Perform PCA on league participant stats w/ colour labelling only for winners
#python rep-learning/pca.py -X league/pickles/X_relevant_stats_winners -o league/results/relevant_participant_stats_role_coloured_winners_pca.png -nc 2 -Y league/pickles/roles_winners

# Perform PCA on league participant stats w/ colour labelling only for winners
#python rep-learning/pca.py -X league/pickles/X_relevant_stats_winners -o league/results/relevant_participant_stats_role_coloured_winners_pca.png -nc 3 -Y league/pickles/roles_winners

# Perform PCA on league participant stats w/ colour labelling only for winners
#python rep-learning/pca.py -X league/pickles/X_relevant_stats_winners -o league/results/relevant_participant_stats_tags_coloured_winners_pca.png -nc 3 -Y league/pickles/tags_winners