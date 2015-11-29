# -*- coding: utf-8 -*-
"""
Script for analyzing match data

@authors : Azwad Sabik, Rohit Bhattacharya
@emails  : azwadsabik@gmail.com, rohit.bhattachar@gmail.com
"""

import pickle
import os
import numpy as np


ENDGAME_PARTICIPANT_STATS = ['assists', 'champLevel', 'deaths', 'doubleKills', 
                                'goldEarned', 'goldSpent', 'inhibitorKills', 
                                'killingSprees', 'kills', 'largestCriticalStrike', 
                                'largestKillingSpree', 'largestMultiKill', 
                                'magicDamageDealt', 'magicDamageDealtToChampions', 
                                'magicDamageTaken', 'minionsKilled', 
                                'neutralMinionsKilled', 
                                'neutralMinionsKilledEnemyJungle', 
                                'neutralMinionsKilledTeamJungle', 
                                'pentaKills', 'physicalDamageDealt', 
                                'physicalDamageDealtToChampions', 
                                'physicalDamageTaken', 'quadraKills', 
                                'sightWardsBoughtInGame', 'totalDamageDealt', 
                                'totalDamageDealtToChampions', 'totalDamageTaken',
                                'totalHeal', 'totalTimeCrowdControlDealt', 
                                'totalUnitsHealed', 'towerKills', 
                                'tripleKills', 'trueDamageDealt', 
                                'trueDamageDealtToChampions', 
                                'trueDamageTaken', 'unrealKills', 
                                'visionWardsBoughtInGame', 
                                'wardsKilled', 'wardsPlaced']
                                
BOOLEAN_PARTICIPANT_STATS = ['firstBloodAssist', 'firstBloodKill',
                             'firstInhibitorAssist', 'firstInhibitorKill',
                             'firstTowerAssist', 'firstTowerKill']


class Match:
    def __init__(self, match):
        self.participants = []
        self.match_duration = match['matchDuration']
        for participant in match['participants']:
            self.participants.append(Participant(participant, self))
    def vectorize_participants(self):
        participants_matrix = np.vstack(tuple([participant.vectorize_stats() 
            for participant in self.participants]))
        return participants_matrix
    def vectorize_winners(self):
        participants_matrix = np.vstack(tuple([participant.vectorize_stats() 
            for participant in self.participants if participant.vectorize_stats()[-1]]))
        return participants_matrix
    def get_match_length(self):
        return self.match_duration

class Participant:
    def __init__(self, participant, match_obj):
        self.stats = participant['stats']
        self.timeline = participant['timeline']
        self.match_obj = match_obj
    def vectorize_stats(self):
        stats_keys = sorted(self.stats.keys())
        stats = []
        for key in stats_keys:
            stats.append(float(self.stats[key]))
        stats = np.array(stats)
        return stats
    def vectorize_timelines(self):
        #This doesn't work
        timeline_keys = sorted(self.timeline.keys())
        timeline_keys = [key for key in timeline_keys if type(self.timeline[key]) == dict]
        timeline_values = []
        for key in timeline_keys:
            timeline_component = self.timeline[key]
            for component_value in timeline_component.values():
                timeline_values.append(component_value)
        timeline_values = np.array(timeline_values)
        return timeline_values
    def vectorize_endgame_stats(self):
        endgame_stats = [self.stats[stat_key] for stat_key in ENDGAME_PARTICIPANT_STATS]
        normalized_endgame_stats = (np.array(endgame_stats, dtype=np.float64)/
                                    self.match_obj.get_match_length())
        return normalized_endgame_stats
    def vectorize_boolean_stats(self):
        boolean_stats = [self.stats[stat_key] for stat_key in BOOLEAN_PARTICIPANT_STATS]
        return np.array(boolean_stats, dtype=np.float64)
    def vectorize_relevant_stats(self):
        return np.hstack((self.vectorize_endgame_stats(), self.vectorize_boolean_stats()))
    def vectorize(self):
        #Don't try this
        return np.hstack((self.vectorize_stats(), self.vectorize_timelines()))

def conditional_load(variable):
    if variable in os.listdir(os.path.join('..', 'pickles')) and variable not in globals():
        with open(os.path.join('..', 'pickles', variable), 'r') as v:
            print "Loading {0}".format(variable)
            globals()[variable] = pickle.load(v)
    return
    
def save(variable):        
    with open(os.path.join('..', 'pickles', variable), 'w') as v:
        pickle.dump(globals()[variable], v)   
        
def generate_X_relevant_stats(match_details):
    match_objects = [Match(match_details[match_key]) for match_key in match_details.keys()] 
    participant_objects = []
    participant_obj_lists = [match_obj.participants for match_obj in match_objects]
    for object_list in participant_obj_lists:
        for participant_obj in object_list:
            participant_objects.append(participant_obj)
    X_relevant_stats = np.vstack(tuple([participant.vectorize_relevant_stats()
                            for participant in participant_objects]))
    with open(os.path.join('..', 'pickles', 'X_relevant_stats'), 'w') as v:
        X_relevant_stats.dump(v)
    return X_relevant_stats
    
if __name__ == "__main__":
    conditional_load('match_details')
    X_relevant_stats = generate_X_relevant_stats(match_details)
    