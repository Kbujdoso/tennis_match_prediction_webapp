import os 
import pandas as pd 
import numpy as np 
from datetime import datetime
import ast 

matches = pd.read_csv("matches_test2.csv")


def flatten_list(x):
    result = []
    if isinstance(x, list):
        for i in range(len(x)):
            result.extend(flatten_list(x[i])) 
    else:
        result.append(x)
    return result
def date_to_unix(x):
        try:
            date = datetime.strptime(str(x).split(".")[0], "%Y%m%d")
            return int(date.timestamp())
        except Exception as e:
            return -1

matches["Player_1_dob"] = matches["Player_1_dob"].apply(date_to_unix)
matches["Player_2_dob"] = matches["Player_2_dob"].apply(date_to_unix)

def hand(x):
    if x == "R":
        return "[1,0]"
    if x == "L":
        return "[0,1]"
    else:
        return "[-1, -1]"

matches["Player_1_hand"] = matches["Player_1_hand"].apply(hand)
matches["Player_2_hand"] = matches["Player_2_hand"].apply(hand)


def surface_func(x):
    if x == "Hard":
        return "[1,0,0,0]"
    elif x == "Clay":
        return "[0,1,0,0]"
    elif x == "Grass": 
        return "[0,0,1,0]"
    elif x == "Carpet": 
        return "[0,0,0,1]"
    
matches["Surface"] = matches["Surface"].apply(surface_func)

matches.to_csv("matches_test.csv", index = False)

def id_to_matches(player, matches): 
    player_matches = matches[
        (matches["Player_1"] == player) | 
        (matches["Player_2"] == player)
        ]
    return player_matches 

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
                prev_match_data.extend([
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
                prev_match_data.extend([
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
        prev_match_data = flatten_list(prev_match_data)
        return prev_match_data
    else:
        prev_match_data = flatten_list(prev_match_data)
        difference = n-num
        for i in range(difference*47):
            prev_match_data.append(-1)
        return prev_match_data
           



def data_set_creator(path_to_csv):

    matches = pd.read_csv(path_to_csv)
    matches["Surface"] = matches["Surface"].apply(surface_func)
    matches["Surface"] = matches["Surface"].apply(ast.literal_eval)
    matches["Player_2_hand"] = matches["Player_2_hand"].apply(hand)
    matches["Player_2_hand"] = matches["Player_2_hand"].apply(ast.literal_eval)
    matches["Player_1_hand"] = matches["Player_1_hand"].apply(hand)
    matches["Player_1_hand"] = matches["Player_1_hand"].apply(ast.literal_eval)
    matches["Court"] = matches["Court"].apply(ast.literal_eval)
    data_set =[]
    data_test = []
    data_train = []
    for i in range(len(matches)):
        print(i)
        match = []
        match.append(matches.loc[i, "Date"]) 
        match.append(matches.loc[i, "Series"])
        match.extend(matches.loc[i, "Court"]) 
        match.extend(matches.loc[i, "Surface"]) 
        match.append(matches.loc[i, "Round"])
        """        for j in range(1, 11):
        match.append(matches.loc[i, f"set_{j}"])"""
        match.extend(matches.loc[i, "Player_1_hand"])
        match.append(matches.loc[i, "Player_1_dob"])
        match.append(matches.loc[i, "Player_1_height"])
        match.extend(matches.loc[i, "Player_2_hand"])
        match.append(matches.loc[i, "Player_2_dob"])
        match.append(matches.loc[i, "Player_2_height"])

        surfaces = ["hard", "clay", "grass", "carpet"]
        for j in range(len(surfaces)):
            match.append(matches.loc[i, f"Player_1_elo_{surfaces[j]}"])
            match.append(matches.loc[i, f"Player_2_elo_{surfaces[j]}"])
            match.append(matches.loc[i, f"Player_1_matches_{surfaces[j]}"])
            match.append(matches.loc[i, f"Player_2_matches_{surfaces[j]}"])

        match.extend(match_history(matches.loc[i, "Player_1"], matches.loc[i,"Date"], matches.loc[i, "Round"], 20, matches))
        match.extend(match_history(matches.loc[i, "Player_2"], matches.loc[i,"Date"], matches.loc[i, "Round"], 20, matches))
        print(len(match))
        #print(match)
        if matches.loc[i, "Player_1"] == matches.loc[i, "Winner"]:
            result = 0
        elif matches.loc[i, "Player_2"] == matches.loc[i, "Winner"]:
            result = 1
        else:
            raise KeyError("Something went wrong")
        data_set.append((match,result))
        """        if matches.loc[i, "Date"] >= 1640995200:
        else: 
            data_train.append((match, result))"""
    return (data_set)
