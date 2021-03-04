# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 10:27:03 2018

@author: maggo
"""

import math

# CONFIGURATION

INITIAL_RATING = 25.0
INITIAL_VOLATILITY = (25 / 3) ** 2
ADDITIONAL_VARIANCE = (25 / 6) ** 2
LOWER_BOUND = 0.0001

'''
(
    (
        (
            ("player name" (string), player rating (float), player volatility (float)),
            ("player name" (string), player rating (float), player volatility (float))
            ...
        ),
        positional ranking (int)
    )
    ...
)
        
SAMPLE_INPUT_1[n]       TEAM n
SAMPLE_INPUT_1[n][0]    TEAM n PLAYERS
SAMPLE_INPUT_1[n][0][m] TEAM n PLAYER m
SAMPLE_INPUT_1[n][0][m][0] TEAM n PLAYER m NAME
SAMPLE_INPUT_1[n][0][m][1] TEAM n PLAYER m RATING
SAMPLE_INPUT_1[n][0][m][2] TEAM n PLAYER m VOLATILITY
SAMPLE_INPUT_1[n][1]    TEAM n POSITIONAL RANKING

PARSED_INPUT[n][2] TEAM n TOTAL RATING
PARSED_INPUT[n][3] TEAM n TOTAL VOLATILITY
'''

SAMPLE_INPUT_1 = (
    (
        (
            ("player1", INITIAL_RATING, INITIAL_VOLATILITY),
            ("player2", INITIAL_RATING, INITIAL_VOLATILITY)
        ),
        1
    ),
    (
        (
            ("player3", INITIAL_RATING, INITIAL_VOLATILITY),
            ("player4", INITIAL_RATING, INITIAL_VOLATILITY)
        ),
        2
    ),
    (
        (
            ("player5", INITIAL_RATING, INITIAL_VOLATILITY),
            ("player6", INITIAL_RATING, INITIAL_VOLATILITY)
        ),
        3
    ),
    (
        (
            ("player7", INITIAL_RATING, INITIAL_VOLATILITY),
            ("player8", INITIAL_RATING, INITIAL_VOLATILITY)
        ),
        4
    ),
)
                
SAMPLE_INPUT_2 = (
    (
        (
            ("player1", 30.892556509887896, 61.728395061728406),
            ("player3", 26.964185503295965, 61.728395061728406)
        ),
        2
    ),
    (
        (
            ("player2", 30.892556509887896, 61.728395061728406),
            ("player5", 23.035814496704035, 61.728395061728406)
        ),
        1
    ),
    (
        (
            ("player4", 26.964185503295965, 61.728395061728406),
            ("player8", 19.107443490112104, 61.728395061728406)
        ),
        4
    ),
    (
        (
            ("player6", 23.035814496704035, 61.728395061728406),
            ("player7", 19.107443490112104, 61.728395061728406)
        ),
        3
    ),
)
                
SAMPLE_INPUT_3 = (
    (
        (
            ('player1', 31.093763569539476, 55.72252451349849),
            ('player4', 22.275817203124628, 55.41378275691641)
        ),
        2
    ),
    (
        (
            ('player2', 35.58092481005924, 55.41378275691641),
            ('player3', 27.165392562947545, 55.72252451349849)
        ),
        4
    ),
    (
        (
            ('player5', 27.724182796875372, 55.41378275691641),
            ('player7', 18.906236430460524, 55.72252451349849)
        ),
        1
    ),
    (
        (
            ('player6', 22.834607437052455, 55.72252451349849),
            ('player8', 14.419075189940767, 55.41378275691641)
        ),
        3
    ),
)
                
SAMPLE_INPUT_4 = (
    (
        (
            ('player1', 32.159214219292735, 50.43753501086132),
            ('player5', 33.57793853028836, 50.187196084576534)
        ),
        1
    ),
    (
        (
            ('player2', 27.95921901437303, 50.961918139605494),
            ('player4', 23.33536451113183, 50.187196084576534)
        ),
        2
    ),
    (
        (
            ('player3', 19.501221901691082, 51.22091395107059),
            ('player6', 23.546957106685706, 51.220913951070585)
        ),
        4
    ),
    (
        (
            ('player7', 24.792606772330476, 50.43753501086131),
            ('player8', 15.127477944206788, 50.961918139605494)
        ),
        3
    ),
)

def calculate_team_strength(players):
    total_rating = 0
    total_volatility = 0
    for player in players:
        total_rating += player[1]
        total_volatility += player[2]
    return (total_rating, total_volatility)

def set_c(volatility_i, volatility_q):
    return (volatility_i + volatility_q + 2 * ADDITIONAL_VARIANCE) ** (1/2)

def probability_i_beats_q(rating_i, rating_q, c):
    e_i = math.e ** (rating_i / c)
    e_q = math.e ** (rating_q / c)
    return e_i / (e_i + e_q)

def skill_update(game_result):
    parsed_result = tuple(
            team + calculate_team_strength(team[0]) for team in game_result
            )
    updated_teams = []
    for i, team in enumerate(parsed_result):
        # team skill update
        deltas = []
        etas = []
        for q, opp in enumerate(parsed_result):
            if q != i:
                c = set_c(team[3], opp[3])
                piq = probability_i_beats_q(team[2], opp[2], c)
                pqi = probability_i_beats_q(opp[2], team[2], c)
                opp_sigma = math.sqrt(opp[3])
                s = 0
                if opp[1] > team[1]:
                    s = 1
                elif opp[1] == team[1]:
                    s = 1/2
                delta_q = (opp[3] / c) * (s - piq)
                gamma_q = opp_sigma / c
                eta_q = gamma_q * (opp[3] / c ** 2) * piq * pqi
                deltas.append(delta_q)
                etas.append(eta_q)
        omega_i = sum(deltas)
        delta_i = sum(etas)
        # individual skill update
        new_strengths = []
        for player in team[0]:
            new_rating = player[1] + (player[2]/team[3]) * omega_i
            new_volatility = player[2] * max(1 - (player[2]/team[3]) * delta_i, LOWER_BOUND)
            new_strengths.append((player[0], new_rating, new_volatility))
        updated_teams.append((tuple(new_strengths), team[1]))
    return tuple(updated_teams)