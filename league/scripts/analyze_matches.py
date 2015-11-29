# -*- coding: utf-8 -*-
"""
Script for analyzing match data

@authors : Azwad Sabik, Rohit Bhattacharya
@emails  : azwadsabik@gmail.com, rohit.bhattachar@gmail.com
"""

import pickle
import os
import numpy as np


class Match:
    def __init__(self, match):
        self.participants = []
        for participant in match['participants']:
            self.participants.append(Participant(participant))
    def vectorize_participants(self):
        participants_matrix = np.vstack(tuple([participant.vectorize_stats() 
            for participant in self.participants]))
        return participants_matrix
    def vectorize_winners(self):
        participants_matrix = np.vstack(tuple([participant.vectorize_stats() 
            for participant in self.participants if participant.vectorize_stats()[-1]]))
        return participants_matrix

class Participant:
    def __init__(self, participant):
        self.stats = participant['stats']
        self.timeline = participant['timeline']
    def vectorize_stats(self):
        stats_keys = sorted(self.stats.keys())
        stats = []
        for key in stats_keys:
            stats.append(float(self.stats[key]))
        stats = np.array(stats)
        return stats
    def vectorize_timelines(self):
        timeline_keys = sorted(self.timeline.keys())
        timeline_keys = [key for key in timeline_keys if type(self.timeline[key]) == dict]
        timeline_values = []
        for key in timeline_keys:
            timeline_component = self.timeline[key]
            for component_value in timeline_component.values():
                timeline_values.append(component_value)
        timeline_values = np.array(timeline_values)
        return timeline_values
    def vectorize(self):
        return np.hstack((self.vectorize_stats(), self.vectorize_timelines()))
            
            

def conditional_load(variable):
    if variable in os.listdir(os.getcwd()) and variable not in globals():
        with open(variable, 'r') as v:
            print "Loading {0}".format(variable)
            globals()[variable] = pickle.load(v)
    return
    
if __name__ == "__main__":
    conditional_load('match_details')