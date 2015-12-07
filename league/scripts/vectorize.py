# -*- coding: utf-8 -*-
"""
Module containing methods for converting RiotWatcher output into manipulable data

@authors : Azwad Sabik, Rohit Bhattacharya
@emails  : azwadsabik@gmail.com, rohit.bhattachar@gmail.com
"""

from league import Match
import numpy as np

def get_match_objects(match_details_dict):        
    match_objects = ([Match(match_details_dict[match_key]) for match_key 
                        in match_details_dict.keys()])
    return match_objects
    
def get_participant_objects(match_details_dict, winners=False, summoner_name=None):        
    match_objects = get_match_objects(match_details_dict)
    participant_objects = []
    participant_obj_lists = [match_obj.participants for match_obj in match_objects]
    for object_list in participant_obj_lists:
        for participant_obj in object_list:
            valid_participant = True
            if winners:
                if not participant_obj.winner:
                    valid_participant = False
            if summoner_name != None:
                if not participant_obj.summoner_name == summoner_name:
                    valid_participant = False
            if valid_participant:
                participant_objects.append(participant_obj)
    return participant_objects
    
def vectorize_participants_relevant_stats(participant_objects):
    relevant_stats = np.vstack(tuple([participant.vectorize_relevant_stats()
                            for participant in participant_objects]))
    return relevant_stats
    
def vectorize_participants_segment_stats(participant_objects, segment_i):
    segment_stats = np.vstack(tuple([participant.vectorize_segment_stats(segment_i)
                            for participant in participant_objects]))
    return segment_stats
    
def generate_lane_labels(participant_objects):
    lanes = [participant_obj.lane for participant_obj in participant_objects]
    return lanes
    
def generate_win_labels(participant_objects):
    wins = [participant_obj.winner for participant_obj in participant_objects]
    return wins
    
def generate_champion_name_labels(participant_objects):
    champion_names = [participant_obj.champion.name for participant_obj in participant_objects]
    return champion_names
    
def generate_champion_primary_tag_labels(participant_objects):
    tags = [participant_obj.champion.tags[0] for participant_obj in participant_objects]
    return tags        
    