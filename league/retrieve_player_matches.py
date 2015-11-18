"""
Script to fetch player match data
using the Riot API

authors : Azwad Sabik, Rohit Bhattacharya
emails  : azwadsabik@gmail.com, rohit.bhattachar@gmail.com
"""

# imports
from riotwatcher import RiotWatcher
import pickle
import random
import numpy as np
import matplotlib.pyplot as plt

# initialize with Riot API key
with open('rohit_league_key.txt', 'r') as f:
     lol = RiotWatcher(f.read().strip())
     
# name of player to retrieve matches for
desired_player_name = 'C9 Sneaky'     
     
# get dictionary of players in challenger league
challenger = lol.get_challenger()

# get player objects
players = challenger['entries']

# iterate through till we find the desired player
for player in players:
    if player['playerOrTeamName'] == desired_player_name:
        desired_player = player

# obtain desired player ID
desired_player_id = player['playerOrTeamId']

# get a list of matches played ranked solo queue
# in a particular season
matches = lol.get_match_list(desired_player_id, ranked_queues='RANKED_SOLO_5x5', 
                         season='SEASON2015')

# get the matchIDs and also
# get labels for role the player played
# in each match (might be useful later)
match_ids = []
role_labels = []
for match in matches['matches']:
     match_ids.append(match['matchId'])
     role_labels.append(match['role'])



