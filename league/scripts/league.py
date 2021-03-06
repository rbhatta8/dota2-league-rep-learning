# -*- coding: utf-8 -*-
"""
Module containing classes for league objects

@authors : Azwad Sabik, Rohit Bhattacharya
@emails  : azwadsabik@gmail.com, rohit.bhattachar@gmail.com
"""

import numpy as np
from data import load

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
                             
RELEVANT_STATS = ENDGAME_PARTICIPANT_STATS + BOOLEAN_PARTICIPANT_STATS

SEGMENTS = ['zeroToTen', 'tenToTwenty', 'twentyToThirty', 'thirtyToEnd']

SEGMENT_STATS = ['kills', 'deaths', 'assists', 'wards', 'towers', 'inhibitors', 
                 'gold', 'level', 'jungle_cs', 'cs', 'damage_taken', 'barons', 
                 'blues', 'reds', 'dragons', 'heralds']
           
champion_id_by_name = load('champion_id_by_name')
champion_data = load('champion_data')
           
class Champion:
    def __init__(self, championId):
        self.data = champion_data[str(championId)]
        self.name = self.data['name']
        self.stats = self.data['stats']
        self.tags = self.data['tags']
    def stats_vector(self):
        vec = np.zeros((1, len(self.stats)))
        stats_keys = self.stats.keys() 
        for i in range(len(self.stats)):
            vec[0, i] = self.stats[stats_keys[i]]
        return vec  
    
class Match:
    def __init__(self, match):
        self.match = match
        self.matchId = match['matchId']
        self.match_duration = match['matchDuration']
        self.frame_interval = match['timeline']['frameInterval']
        self.frames = match['timeline']['frames']
        self.participant_identities = match['participantIdentities']
        self.participants = [Participant(participant, self) for participant in
            match['participants']]
    def vectorize_participants(self):
        participants_matrix = np.vstack(tuple([participant.vectorize_stats() 
            for participant in self.participants]))
        return participants_matrix
    def vectorize_winners(self):
        participants_matrix = np.vstack(tuple([participant.vectorize_stats() 
            for participant in self.participants if participant.vectorize_stats()[-1]]))
        return participants_matrix
    def get_summoner_name(self, participantId):
        name = ""
        for identity in self.participant_identities:
            if identity['participantId'] == participantId:
                name = identity['player']['summonerName']
        return name
    def get_participantFrames(self, participantId):
        participantFrames = {}
        for frame in self.frames:
            participantFrames[frame['timestamp']] = frame['participantFrames'][str(participantId)]
        return participantFrames
    def get_events(self, participantId=None):
        events = []
        for frame in self.frames[1:]:
            if 'events' in frame.keys():
                events.extend(frame['events'])
        if participantId != None:
            events = [event for event in events if self.participant_involved(event, participantId)]
        return events
    def participant_involved(self, event, participantId):
        truth = False
        if 'participantId' in event.keys():
            truth = True if (event['participantId'] == participantId) else False
        if 'killerId' in event.keys() and not truth:
            truth = True if (event['killerId'] == participantId) else False
        if 'victimId' in event.keys() and not truth:
            truth = True if (event['victimId'] == participantId) else False
        if 'assistingParticipantIds' in event.keys() and not truth:
            truth = True if (participantId in event['assistingParticipantIds']) else False
        if 'creatorId' in event.keys() and not truth:
            truth = True if (event['creatorId'] == participantId) else False
        return truth
        
class Participant:
    def __init__(self, participant, match_obj):
        self.participantId = participant['participantId']
        self.championId = participant['championId']
        self.champion = Champion(self.championId)
        self.stats = participant['stats']
        self.timeline = participant['timeline']
        self.frame_interval = match_obj.frame_interval
        self.summoner_name = match_obj.get_summoner_name(self.participantId)
        self.participantFrames = match_obj.get_participantFrames(self.participantId)
        self.events = match_obj.get_events(participantId=self.participantId)
        self.lane = self.timeline['lane']
        self.role = self.timeline['role']
        self.winner = int(self.stats['winner'])
        self.match_obj = match_obj
    def vectorize_stats(self):
        stats_keys = sorted(self.stats.keys())
        stats = []
        for key in stats_keys:
            stats.append(float(self.stats[key]))
        stats = np.array(stats)
        return stats
    def vectorize_endgame_stats(self):
        endgame_stats = [self.stats[stat_key] for stat_key in ENDGAME_PARTICIPANT_STATS]
        normalized_endgame_stats = (np.array(endgame_stats, dtype=np.float64)/
                                    self.match_obj.match_duration)
        return normalized_endgame_stats
    def vectorize_boolean_stats(self):
        boolean_stats = [self.stats[stat_key] for stat_key in BOOLEAN_PARTICIPANT_STATS]
        return np.array(boolean_stats, dtype=np.float64)
    def vectorize_relevant_stats(self):
        return np.hstack((self.vectorize_endgame_stats(), self.vectorize_boolean_stats()))
    def get_segment_stats(self, segment_i):
        """
        Vectorize stats for i-th segment of match        
        """
        stats = dict(zip(SEGMENT_STATS, [0]*len(SEGMENT_STATS)))
        if segment_i == -1:
            return stats
        previous_stats = self.get_segment_stats(segment_i - 1)
        t_i, t_f = segment_i*10*self.frame_interval, (segment_i + 1)*10*self.frame_interval
        stats = previous_stats
        for event in self.events:
            if t_i < event['timestamp'] < t_f:
                event_type = self.classify_event(event)
            else: 
                event_type = None
            if event_type != None:
                stats[event_type] += 1
        segment_name = SEGMENTS[segment_i]
        if segment_i < self.match_obj.match_duration/60/10:
            stats['gold'] += self.timeline['goldPerMinDeltas'][segment_name]*10
            stats['damage_taken'] += self.timeline['damageTakenPerMinDeltas'][segment_name]*10
        latest_frame = None
        latest_frame_key = 0
        for k, v in sorted(self.participantFrames.items()):
            latest_frame_key = k if k < t_f else latest_frame_key
            latest_frame = self.participantFrames[k]
            if k > t_f:
                break
        stats['jungle_cs'] = latest_frame['jungleMinionsKilled']
        stats['cs'] = latest_frame['minionsKilled']
        stats['level'] = latest_frame['level']
        return stats
    def vectorize_segment_stats(self, segment_i):
        stats = self.get_segment_stats(segment_i)
        stats_vector = np.zeros((1, len(SEGMENT_STATS)))
        for i, v in enumerate(SEGMENT_STATS):
            stats_vector[0, i] = stats[v] 
        return stats_vector
    def classify_event(self, event):
        if event['eventType'] == 'CHAMPION_KILL':
            if event['killerId'] == self.participantId:
                return 'kills'
            elif event['victimId'] == self.participantId:
                return 'deaths'
            elif self.participantId in event['assistingParticipantIds']:
                return 'assists'
            else:
                return None
        elif event['eventType'] =='BUILDING_KILL':
            if event['buildingType'] == 'TOWER_BUILDING':
                return 'towers'
            elif event['buildingType'] == 'INHIBITOR_BUILDING':
                return 'inhibitors'
            else: 
                return None
        elif event['eventType'] == 'WARD_PLACED':
            if event['creatorId'] == self.participantId:
                return 'wards'
            else:
                return None
        elif event['eventType'] == 'ELITE_MONSTER_KILL':
            if event['monsterType'] == 'DRAGON':
                return 'dragons'
            elif event['monsterType'] == 'BARON_NASHOR':
                return 'barons'
            elif event['monsterType'] == 'BLUE_GOLEM':
                return 'blues'
            elif event['monsterType'] == 'RED_LIZARD':
                return 'reds'
            elif event['monsterType'] == 'RIFTHERALD':
                return 'heralds'
            else:
                return None
        else:
            return None
