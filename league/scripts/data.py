# -*- coding: utf-8 -*-
"""
Module for data read, write, and retrieval operations

@authors : Azwad Sabik, Rohit Bhattacharya
@emails  : azwadsabik@gmail.com, rohit.bhattachar@gmail.com
"""

from riotwatcher import RiotWatcher as RW
import pickle
import time
import os
import random

PICKLE_DIR = os.path.join('..', 'pickles')
KEYS_DIR = os.path.join('..', 'keys')
REQUEST_DELAY = 3

def load(fn):
    """
    Load and return variable stored in pickle named fn
    """
    with open(os.path.join(PICKLE_DIR, fn), 'rb') as fp:
        print "Loading {0}".format(fn)
        variable = pickle.load(fp)
    return variable

def save(variable, fn):
    """
    Save variable to pickle named fn
    """
    with open(os.path.join(PICKLE_DIR, fn), 'wb') as fp:
        print "Saving {0}".format(fn)
        pickle.dump(variable, fp)
        
class Retriever:
    def __init__(self, keys = None):
        if keys == None:
            self.keys = os.listdir(KEYS_DIR)
        else:
            self.keys = keys
        self.handles = []
        for key in self.keys:
            with open(os.path.join(KEYS_DIR, key), 'r') as fp:
                self.handles.append(RW(fp.read().strip()))
        self.current_handle_index = random.randint(0, len(self.keys) - 1)
    def get_active_handle(self):
        time.sleep(REQUEST_DELAY)
        self.current_handle_index += 1
        self.current_handle_index %= len(self.handles)
        active_handle = None
        while active_handle == None:
            current_handle = self.handles[self.current_handle_index]
            if current_handle.can_make_request():
                active_handle = current_handle
            else:
                time.sleep(REQUEST_DELAY)
                self.current_handle_index += 1
                self.current_handle_index %= len(self.handles)
        return active_handle
    def retrieve_champion_id_by_name(self):
        lol = self.get_active_handle()
        info = lol.static_get_champion_list()
        champions = info['data']
        names = champions.keys()
        ids = [champion['id'] for champion in champions.values()]
        champion_id_by_name = dict(zip(names, ids))
        return champion_id_by_name
    def retrieve_champion_data(self):
        lol = self.get_active_handle()
        info = lol.static_get_champion_list(data_by_id = True, 
                                                     champ_data = 'all')
        champion_data = info['data']
        return champion_data
    def retrieve_challenger_player_names(self):
        lol = self.get_active_handle()
        player_names = []
        # make request for list of players in challenger league
        challenger = lol.get_challenger()
        # collect player names
        for player in challenger['entries']:
            player_names.append(player['playerOrTeamName'])
        return player_names
    def retrieve_player_match_list(self, player_name):
        print "Loading match list for {0} [API KEY: {1}]".format(player_name, 
                self.keys[self.current_handle_index])
        lol = self.get_active_handle()
        # determine summoner id of query player
        summoner_id = lol.get_summoner(name=player_name)['id']
        # make request for player's matches
        match_list = lol.get_match_list(summoner_id)['matches']
        return match_list
    def retrieve_match_details(self, match=None):
        lol = self.get_active_handle()
        # get match id
        match_id = match['matchId']
        # make request for match details
        details = lol.get_match(match_id, include_timeline=True)
        return details
    def retrieve_player_match_details(self, player_name, m_f, m_i = 0, match_list = None):
        if match_list == None:        
            match_list = self.retrieve_player_match_list(player_name)
        matches = {}
        m_i = m_i if len(match_list) >= m_i else len(match_list)
        m_f = m_f if len(match_list) >= m_f else len(match_list)
        for i, match in enumerate(match_list[m_i:m_f]):
            matchId = match['matchId']
            print "Loading match {0}: #{1} of {2} for Player {3} [API KEY: {4}]".format(
                matchId, i + 1, m_f - m_i, player_name, self.keys[self.current_handle_index])
            matches[matchId] = self.retrieve_match_details(match)
        return matches

