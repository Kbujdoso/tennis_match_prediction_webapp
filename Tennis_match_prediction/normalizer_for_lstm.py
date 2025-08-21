import os 
import pandas as pd 
import numpy as np 
from datetime import datetime
import ast 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
matches = pd.read_csv(os.path.join(BASE_DIR,"matches.csv"))


def flatten_list(x):
    result = []
    if isinstance(x, list):
        for i in range(len(x)):
            result.extend(flatten_list(x[i])) 
    else:
        result.append(x)
    return result

def safe_eval(x):
    if isinstance(x, str):
        try:
            return ast.literal_eval(x)
        except Exception:
            return x 
    else:
        return x


def id_to_matches(player, matches): 
    player_matches = matches[
        (matches["Player_1"] == player) | 
        (matches["Player_2"] == player)
        ]
    return player_matches 
@staticmethod
def match_history_for_main(id, date, round, n, matches): 
    matches["Surface"] = matches["Surface"].apply(safe_eval)
    matches["Player_2_hand"] = matches["Player_2_hand"].apply(safe_eval)
    matches["Player_1_hand"] = matches["Player_1_hand"].apply(safe_eval)
    matches["Court"] = matches["Court"].apply(safe_eval)
    matches_filtered = id_to_matches(id, matches)
    prev_match_data = []
    matches_filtered = matches_filtered.sort_values(by=["Date", "Round"])
    num = 0
    for i in range(len(matches_filtered)):
        row = matches_filtered.iloc[i]
        if row["Winner"] == id:
            result = 1
        else:
            result = 0
        if row["Date"] == date and row["Round"] == round or num == n:
            break
        else:
            num = num + 1 
            if row["Player_1"] == id:
                prev_match_data.append([
                    row["Date"],
                    row["Series"],
                    row["Court"],
                    row["Surface"],
                    row["Round"],
                    row["Best of"],
                    row["Rank_1"],
                    row["Rank_2"],
                    row["Pts_1"],
                    row["Pts_2"],
                    row["Odd_1"],
                    row["Odd_2"],
                    row["set_1"],
                    row["set_2"],
                    row["set_3"],
                    row["set_4"],
                    row["set_5"],
                    row["set_6"],
                    row["set_7"],
                    row["set_8"],
                    row["set_9"],
                    row["set_10"],
                    row["Player_1_hand"],
                    row["Player_1_dob"],
                    row["Player_1_height"],
                    row["Player_1_elo_hard"],
                    row["Player_1_elo_clay"],
                    row["Player_1_elo_grass"],
                    row["Player_1_elo_carpet"],
                    row["Player_1_matches_hard"],
                    row["Player_1_matches_clay"],
                    row["Player_1_matches_grass"],
                    row["Player_1_matches_carpet"],
                    row["Player_2_hand"],
                    row["Player_2_dob"],
                    row["Player_2_height"],
                    row["Player_2_elo_hard"],
                    row["Player_2_elo_clay"],
                    row["Player_2_elo_grass"],
                    row["Player_2_elo_carpet"],
                    row["Player_2_matches_hard"],
                    row["Player_2_matches_clay"],
                    row["Player_2_matches_grass"],
                    row["Player_2_matches_carpet"],
                    result])
                
            elif row["Player_2"] == id: 
                prev_match_data.append([
                    row["Date"],
                    row["Series"],
                    row["Court"],
                    row["Surface"],
                    row["Round"],
                    row["Best of"],
                    row["Rank_2"],
                    row["Rank_1"],
                    row["Pts_2"],
                    row["Pts_1"],
                    row["Odd_2"],
                    row["Odd_1"],
                    row["set_2"],
                    row["set_1"],
                    row["set_4"],
                    row["set_3"],
                    row["set_6"],
                    row["set_5"],
                    row["set_8"],
                    row["set_7"],
                    row["set_10"],
                    row["set_9"],
                    row["Player_2_hand"],
                    row["Player_2_dob"],
                    row["Player_2_height"],
                    row["Player_2_elo_hard"],
                    row["Player_2_elo_clay"],
                    row["Player_2_elo_grass"],
                    row["Player_2_elo_carpet"],
                    row["Player_2_matches_hard"],
                    row["Player_2_matches_clay"],
                    row["Player_2_matches_grass"],
                    row["Player_2_matches_carpet"],
                    row["Player_1_hand"],
                    row["Player_1_dob"],
                    row["Player_1_height"],
                    row["Player_1_elo_hard"],
                    row["Player_1_elo_clay"],
                    row["Player_1_elo_grass"],
                    row["Player_1_elo_carpet"],
                    row["Player_1_matches_hard"],
                    row["Player_1_matches_clay"],
                    row["Player_1_matches_grass"],
                    row["Player_1_matches_carpet"],
                    result
                ])
                

    if num == n:
        for i in range(len(prev_match_data)):
            prev_match_data[i] = flatten_list(prev_match_data[i])
        return prev_match_data[::-1]
    else:
        for i in range(len(prev_match_data)):
            prev_match_data[i] = flatten_list(prev_match_data[i])
        difference = n-num
        for _ in range(difference):
            no_history = [-1.0] * 51
            prev_match_data.append(no_history)
        return prev_match_data[::-1]
           
def match_history(id, date, round, n, matches): 
    matches_filtered = id_to_matches(id, matches)
    prev_match_data = []
    matches_filtered = matches_filtered.sort_values(by=["Date", "Round"])
    num = 0
    for i in range(len(matches_filtered)):
        row = matches_filtered.iloc[i]
        if row["Winner"] == id:
            result = 1
        else:
            result = 0
        if row["Date"] == date and row["Round"] == round or num == n:
            break
        else:
            num = num + 1 
            if row["Player_1"] == id:
                prev_match_data.append([
                    row["Date"],
                    row["Series"],
                    row["Court"],
                    row["Surface"],
                    row["Round"],
                    row["Best of"],
                    row["Rank_1"],
                    row["Rank_2"],
                    row["Pts_1"],
                    row["Pts_2"],
                    row["Odd_1"],
                    row["Odd_2"],
                    row["set_1"],
                    row["set_2"],
                    row["set_3"],
                    row["set_4"],
                    row["set_5"],
                    row["set_6"],
                    row["set_7"],
                    row["set_8"],
                    row["set_9"],
                    row["set_10"],
                    row["Player_1_hand"],
                    row["Player_1_dob"],
                    row["Player_1_height"],
                    row["Player_1_elo_hard"],
                    row["Player_1_elo_clay"],
                    row["Player_1_elo_grass"],
                    row["Player_1_elo_carpet"],
                    row["Player_1_matches_hard"],
                    row["Player_1_matches_clay"],
                    row["Player_1_matches_grass"],
                    row["Player_1_matches_carpet"],
                    row["Player_2_hand"],
                    row["Player_2_dob"],
                    row["Player_2_height"],
                    row["Player_2_elo_hard"],
                    row["Player_2_elo_clay"],
                    row["Player_2_elo_grass"],
                    row["Player_2_elo_carpet"],
                    row["Player_2_matches_hard"],
                    row["Player_2_matches_clay"],
                    row["Player_2_matches_grass"],
                    row["Player_2_matches_carpet"],
                    result])
                
            elif row["Player_2"] == id: 
                prev_match_data.append([
                    row["Date"],
                    row["Series"],
                    row["Court"],
                    row["Surface"],
                    row["Round"],
                    row["Best of"],
                    row["Rank_2"],
                    row["Rank_1"],
                    row["Pts_2"],
                    row["Pts_1"],
                    row["Odd_2"],
                    row["Odd_1"],
                    row["set_2"],
                    row["set_1"],
                    row["set_4"],
                    row["set_3"],
                    row["set_6"],
                    row["set_5"],
                    row["set_8"],
                    row["set_7"],
                    row["set_10"],
                    row["set_9"],
                    row["Player_2_hand"],
                    row["Player_2_dob"],
                    row["Player_2_height"],
                    row["Player_2_elo_hard"],
                    row["Player_2_elo_clay"],
                    row["Player_2_elo_grass"],
                    row["Player_2_elo_carpet"],
                    row["Player_2_matches_hard"],
                    row["Player_2_matches_clay"],
                    row["Player_2_matches_grass"],
                    row["Player_2_matches_carpet"],
                    row["Player_1_hand"],
                    row["Player_1_dob"],
                    row["Player_1_height"],
                    row["Player_1_elo_hard"],
                    row["Player_1_elo_clay"],
                    row["Player_1_elo_grass"],
                    row["Player_1_elo_carpet"],
                    row["Player_1_matches_hard"],
                    row["Player_1_matches_clay"],
                    row["Player_1_matches_grass"],
                    row["Player_1_matches_carpet"],
                    result
                ])
                

    if num == n:
        for i in range(len(prev_match_data)):
            prev_match_data[i] = flatten_list(prev_match_data[i])
        return prev_match_data[::-1]
    else:
        for i in range(len(prev_match_data)):
            prev_match_data[i] = flatten_list(prev_match_data[i])
        difference = n-num
        for _ in range(difference):
            no_history = [-1.0] * 51
            prev_match_data.append(no_history)
        return prev_match_data[::-1]
           


def data_set_creator_lstm(path_to_csv):

    matches = pd.read_csv(path_to_csv)
    matches["Surface"] = matches["Surface"].apply(ast.literal_eval)
    matches["Player_2_hand"] = matches["Player_2_hand"].apply(ast.literal_eval)
    matches["Player_1_hand"] = matches["Player_1_hand"].apply(ast.literal_eval)
    matches["Court"] = matches["Court"].apply(ast.literal_eval)
    data_set =[]
    for i in range(len(matches)):
        print(i)
        player_features = []
        player_features.append(matches.loc[i, "Date"]) 
        player_features.append(matches.loc[i, "Series"])
        player_features.extend(matches.loc[i, "Court"]) 
        player_features.extend(matches.loc[i, "Surface"]) 
        player_features.append(matches.loc[i, "Round"])
        player_features.extend(matches.loc[i, "Player_1_hand"])
        player_features.append(matches.loc[i, "Player_1_dob"])
        player_features.append(matches.loc[i, "Player_1_height"])
        player_features.extend(matches.loc[i, "Player_2_hand"])
        player_features.append(matches.loc[i, "Player_2_dob"])
        player_features.append(matches.loc[i, "Player_2_height"])

        surfaces = ["hard", "clay", "grass", "carpet"]
        for j in range(len(surfaces)):
            player_features.append(matches.loc[i, f"Player_1_elo_{surfaces[j]}"])
            player_features.append(matches.loc[i, f"Player_2_elo_{surfaces[j]}"])
            player_features.append(matches.loc[i, f"Player_1_matches_{surfaces[j]}"])
            player_features.append(matches.loc[i, f"Player_2_matches_{surfaces[j]}"])

        player_history_1 =(match_history(matches.loc[i, "Player_1"], matches.loc[i,"Date"], matches.loc[i, "Round"], 30, matches))
        player_history_2 =(match_history(matches.loc[i, "Player_2"], matches.loc[i,"Date"], matches.loc[i, "Round"], 30, matches))

        if matches.loc[i, "Player_1"] == matches.loc[i, "Winner"]:
            result = 0
        elif matches.loc[i, "Player_2"] == matches.loc[i, "Winner"]:
            result = 1
        else:
            raise KeyError("Something went wrong")
        data_set.append(((player_features, player_history_1, player_history_2),result))

    return (data_set)
