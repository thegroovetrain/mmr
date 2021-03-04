# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 09:40:51 2018

@author: maggo
"""

import math

INITIAL_MU = 25
INITIAL_SIGMA_SQUARED = (25/3) ** 2
BETA_SQUARED = (25/6) ** 2
KAPPA = 0.0001

test_player_1 = (INITIAL_MU, INITIAL_SIGMA_SQUARED)
test_player_2 = (INITIAL_MU, INITIAL_SIGMA_SQUARED)
test_player_3 = (INITIAL_MU, INITIAL_SIGMA_SQUARED)
test_player_4 = (INITIAL_MU, INITIAL_SIGMA_SQUARED)
test_player_5 = (INITIAL_MU, INITIAL_SIGMA_SQUARED)
test_player_6 = (INITIAL_MU, INITIAL_SIGMA_SQUARED)
test_player_7 = (INITIAL_MU, INITIAL_SIGMA_SQUARED)
test_player_8 = (INITIAL_MU, INITIAL_SIGMA_SQUARED)

test_team_1_players = (test_player_1, test_player_2)
test_team_2_players = (test_player_3, test_player_4)
test_team_3_players = (test_player_5, test_player_6)
test_team_4_players = (test_player_7, test_player_8)

def set_gamma(sigma, c):    #sigma[i]/c[i][q]
    return sigma/c

def set_team_mu(team):
    team_mu = 0
    for player in team:
        team_mu += player[0]
    return team_mu

test_team_1_mu = set_team_mu(test_team_1_players)
test_team_2_mu = set_team_mu(test_team_2_players)
test_team_3_mu = set_team_mu(test_team_3_players)
test_team_4_mu = set_team_mu(test_team_4_players)

def set_team_sigma_squared(team):
    team_sigma_squared = 0
    for player in team:
        team_sigma_squared += player[1]
    return team_sigma_squared

test_team_1_sigma_squared = set_team_sigma_squared(test_team_1_players)
test_team_2_sigma_squared = set_team_sigma_squared(test_team_2_players)
test_team_3_sigma_squared = set_team_sigma_squared(test_team_3_players)
test_team_4_sigma_squared = set_team_sigma_squared(test_team_4_players)

def set_c(team_i_sigma_squared, team_q_sigma_squared):
    return (team_i_sigma_squared + team_q_sigma_squared + 2 * BETA_SQUARED) ** (1/2)

def set_p(team_i_mu, team_q_mu, c):
    e_i = math.e ** (team_i_mu / c)
    e_q = math.e ** (team_q_mu / c)
    return e_i / (e_i + e_q)

test_team_1 = (test_team_1_players, test_team_1_mu, test_team_1_sigma_squared)
test_team_2 = (test_team_2_players, test_team_2_mu, test_team_2_sigma_squared)
test_team_3 = (test_team_3_players, test_team_3_mu, test_team_3_sigma_squared)
test_team_4 = (test_team_4_players, test_team_4_mu, test_team_4_sigma_squared)

test_game_result_1 = ((test_team_1, 1), (test_team_2, 2), (test_team_3, 3), (test_team_4, 4))

def set_delta(team_sigma_squared, c, s, p):
    return (team_sigma_squared / c) * (s - p)

def set_eta(gamma, sigma, c, p_iq, p_qi):
    return gamma * (sigma / c) ** 2 * p_iq * p_qi

def set_Omega(deltas):
    return sum(deltas)

def set_Delta(etas):
    return sum(etas)

def calculate_team_strength(team):
    return (set_team_mu(team), set_team_sigma_squared(team))