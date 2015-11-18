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


# get 10 match info first (50 gives too many request error)
for match_id in match_ids[:-10]:

     # get a match by IDs gathered from before
     match = lol.get_match(match_id, include_timeline=True)

     # get stats of each participant
     participant_stats = match['participants']
     
     # print len(participant_stats)
     # find the participantID for the desired player
     #print match['participantIdentities']
     for players in match['participantIdentities']:
          print players['player']['summonerId'], desired_player_id
          print players['player']['summonerName'], desired_player_name

          # tried to check by summoner ID, this never seems to give a match
          if players['player']['summonerId'] == desired_player_id:
               print players['player']['summonerName']

          # now checking by summoner name
          if players['player']['summonerName'] == desired_player_name:
               print players['player']['summonerName']

     break
     
