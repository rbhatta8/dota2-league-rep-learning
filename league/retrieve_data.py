# -*- coding: utf-8 -*-
"""
Script for collecting raw match data

@authors : Azwad Sabik, Rohit Bhattacharya
@emails  : azwadsabik@gmail.com, rohit.bhattachar@gmail.com
"""

from riotwatcher import RiotWatcher
import pickle
import time
import os

pickle_vars = ['challenger_matches', 'match_details']
# challenger_matches is dictionary: {player_name : match_list}
# match_details is dictionary: {match_id : details}

api_key_filenames = ['Veraxios.txt', 'Sabikan.txt', 'teasogood.txt']
api_handles = []
for fn in api_key_filenames:
    with open(fn, 'r') as fp:
        api_key = fp.read().strip()
        api_handles.append(RiotWatcher(api_key))

current_handle_index = 0        
        
def conditional_load(variable):
    if variable in os.listdir(os.getcwd()) and variable not in globals():
        with open(variable, 'r') as v:
            print "Loading {0}".format(variable)
            globals()[variable] = pickle.load(v)
    return
        
def save(variable):        
    with open(variable, 'w') as v:
        pickle.dump(globals()[variable], v)        
        
def get_active_handle():
    time.sleep(3)
    global current_handle_index
    current_handle_index += 1
    current_handle_index %= len(api_handles)
    active_handle = None
    while active_handle == None:
        current_handle = api_handles[current_handle_index]
        if current_handle.can_make_request():
            active_handle = current_handle
            #print current_handle_index, current_handle.can_make_request()
        else:
            #print current_handle_index, current_handle.can_make_request()
            time.sleep(1.5)
            current_handle_index += 1
            current_handle_index %= len(api_handles)
    return active_handle
    
def retrieve_challenger_player_names():
    lol = get_active_handle()
    player_names = []
    # make request for list of players in challenger league
    challenger = lol.get_challenger()
    # collect player names
    for player in challenger['entries']:
        player_names.append(player['playerOrTeamName'])
    return player_names
    
def retrieve_player_matches(player_name):
    lol = get_active_handle()
    # determine summoner id of query player
    summoner_id = lol.get_summoner(name=player_name)['id']
    # make request for player's matches
    matches = lol.get_match_list(summoner_id)['matches']
    return matches
            
def retrieve_match_details(match=None, ):
    lol = get_active_handle()
    # get match id
    match_id = match['matchId']
    # make request for match details
    details = lol.get_match(match_id, include_timeline=True)
    return details
            
for variable in pickle_vars:
    conditional_load(variable)
    
if __name__ == '__main__':
    if 'challenger_matches' not in vars():
        print "Retrieving Challenger Names"
        challengers_names = retrieve_challenger_player_names()
        challenger_matches = {}
        for name in challengers_names:
            challenger_matches[name] = []
        save('challenger_matches')
    for player_name in challenger_matches.keys():
        player_index = challenger_matches.keys().index(player_name)
        if challenger_matches[player_name] == []:
            challenger_matches[player_name] = retrieve_player_matches(player_name)
            print "Retrieving Matches for Player {2} ({0}) [API KEY: {1}]".format(
                    player_name, current_handle_index, player_index)
    save('challenger_matches')
    if 'match_details' not in vars():
        match_details = {}
        save('match_details')
    matches_per_player = 5
    for player_name in challenger_matches.keys():
        n_matches_loaded = 0
        player_index = challenger_matches.keys().index(player_name)
        matches = challenger_matches[player_name]
        while n_matches_loaded < matches_per_player:
            current_match = matches[n_matches_loaded]
            current_match_id = current_match['matchId']
            if current_match_id not in match_details.keys():
                match_details[current_match_id] = retrieve_match_details(
                                                    current_match)
                print "Loading match {0}: #{1} of {2} for Player {3} ({4}) [API KEY: {5}]".format(
                        current_match_id, n_matches_loaded, matches_per_player,
                        player_index, player_name, current_handle_index)
            n_matches_loaded += 1
            if n_matches_loaded >= len(matches):
                break
    save('match_details')
            
            
                    
                