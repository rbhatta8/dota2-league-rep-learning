"""
Script to fetch player match data
using the Riot API

authors : Azwad Sabik, Rohit Bhattacharya
emails  : azwadsabik@gmail.com, rohit.bhattachar@gmail.com
"""

# imports
from riotwatcher import *
import pickle
import random
import numpy as np
import matplotlib.pyplot as plt

# initialize with Riot API key
with open('Sabikan_API_Key.txt', 'r') as f:
     lol = RiotWatcher(f.read().strip())

def keyA():
    global lol
    with open('rohit_league_key.txt', 'r') as f:
     lol = RiotWatcher(f.read().strip())

def keyB():
    global lol
    with open('Sabikan_API_Key.txt', 'r') as f:
     lol = RiotWatcher(f.read().strip())
     
def keyC():
    global lol
    with open('Veraxios_API_Key.txt', 'r') as f:
     lol = RiotWatcher(f.read().strip())
          
keys = [keyA, keyB, keyC]

def retrieve_challenger_player_names():
    player_names = []
    # make request for list of players in challenger league
    challenger = lol.get_challenger()
    # collect player names
    for player in challenger['entries']:
        player_names.append(player['playerOrTeamName'])
    return player_names

def retrieve_player_matches(player_name):
    # determine summoner id of query player
    summoner_id = lol.get_summoner(name=player_name)['id']
    # make request for player's matches
    matches = lol.get_match_list(summoner_id)['matches']
    
    return matches
    
def retrieve_player_match_info(player_name, match):
    # get match id
    match_id = match['matchId']
    # make request for match details
    match = lol.get_match(match_id)
    # determine player's in-game participant Id
    participant_identities = match['participantIdentities']
    for participant in participant_identities:
        participant_name = participant['player']['summonerName']
        if participant_name == player_name:
            player_participant_id = participant['participantId']
            break
    # get player's match information
    player_match_info = match['participants'][player_participant_id - 1]
    return player_match_info

def vectorize_player_match_stats(player_match_info):
    stats = player_match_info['stats']
    n_stats = len(stats)
    stats_vector = np.zeros((1, n_stats))
    stats_keys = stats.keys()
    for i in range(n_stats):
        stats_vector[0, i] = stats[stats_keys[i]]
    return stats_vector
        
def retrieve_player_match_stats(desired_player_name, first_ind, last_ind):   
    desired_player_matches = retrieve_player_matches(desired_player_name)
    recent_matches = desired_player_matches[first_ind:last_ind]
    recent_stats = None
    for match in recent_matches:
        match_info = retrieve_player_match_info(desired_player_name, 
                                               match)
        match_stats = vectorize_player_match_stats(match_info)
        print match_stats
        if recent_stats == None:
            recent_stats = match_stats
        else:
            recent_stats = np.vstack((recent_stats, match_stats))
    return recent_stats

def test(desired_player_name):
    X = None
    for i in range(3):
        first_ind = i*5
        last_ind = first_ind + 5
        key_func = keys[i%3]
        x_out = retrieve_player_match_stats(desired_player_name, first_ind, last_ind)
        if X == None:        
            X = x_out
        else:
            X = np.vstack((X, x_out))
        key_func()
    return X
            
X = test('C9 Sneaky')
n_samples, n_features = X.shape

# Locally linear embedding of the dataset
print("Computing LLE embedding")
n_neighbors = 2
clf = manifold.LocallyLinearEmbedding(n_neighbors, n_components=2,
                                      method='standard')                                     
X_lle = clf.fit_transform(X)
print("Done. Reconstruction error: %g" % clf.reconstruction_error_)

plt.title('LLE')
plt.scatter(X_lle[:, 0], X_lle[:, 1])