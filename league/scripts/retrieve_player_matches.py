# -*- coding: utf-8 -*-
"""
Script for retrieving player participant data and generating pickles of
numpy arrays representing the participant data (for recent matches)

@authors : Azwad Sabik, Rohit Bhattacharya
@emails  : azwadsabik@gmail.com, rohit.bhattachar@gmail.com
"""

import data
import vectorize

SUMMONER_NAME = 'C9 Sneaky'
NUMBER_OF_MATCHES = 5

if __name__ == "__main__":    
    r = data.Retriever()
    md = r.retrieve_player_match_details(SUMMONER_NAME, NUMBER_OF_MATCHES)
    data.save(md, SUMMONER_NAME + '_match_details_dict')
    po = vectorize.get_participant_objects(md, summoner_name = SUMMONER_NAME)
    po_win = vectorize.get_participant_objects(md, winners = True,
                                                   summoner_name = SUMMONER_NAME)
    rs = vectorize.vectorize_participants_relevant_stats(po)
    rs_win = vectorize.vectorize_participants_relevant_stats(po_win)
    s0 = vectorize.vectorize_participants_segment_stats(po, 0)
    s0_win = vectorize.vectorize_participants_segment_stats(po_win, 0)
    s1 = vectorize.vectorize_participants_segment_stats(po, 1)
    s1_win = vectorize.vectorize_participants_segment_stats(po_win, 1)
    data.save(rs, SUMMONER_NAME + '_relevant_stats')
    data.save(rs_win, SUMMONER_NAME + '_relevant_stats_wins')
    data.save(s0, SUMMONER_NAME + '_segment_0_stats')
    data.save(s0_win, SUMMONER_NAME + '_segment_0_stats_wins')
    data.save(s1, SUMMONER_NAME + '_segment_1_stats')
    data.save(s1_win, SUMMONER_NAME + '_segment_1_stats_wins')