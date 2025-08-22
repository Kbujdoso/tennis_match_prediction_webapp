import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import sys

# sys.stderr = open(os.devnull, 'w')
from keras.models import load_model
import numpy as np
import pandas as pd
from datetime import datetime
from .normalizer_for_lstm import match_history_for_main
from .database import Court, Series, flatten_list
import ast 


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
matches = pd.read_csv(os.path.join(BASE_DIR, "matches.csv"))
player_elos = pd.read_csv(os.path.join(BASE_DIR, "players_elo.csv"))
players_stats = pd.read_csv(os.path.join(BASE_DIR, "player_features.csv"))

def date_to_unix(x):
        try:
            date = datetime.strptime(str(x).split(".")[0], "%Y%m%d")
            return int(date.timestamp())
        except Exception as e:
            return -1
        
def hand(x):
    if x == "R":
        return [1,0]
    if x == "L":
        return [0,1]
    else:
        return [-1, -1]
def surface_func(x):
    if x == "Hard":
        return [1,0,0,0]
    elif x == "Clay":
        return [0,1,0,0]
    elif x == "Grass": 
        return [0,0,1,0]
    elif x == "Carpet": 
        return [0,0,0,1]
def name_id(name):
    player = player_elos[player_elos['name'] == name]
    if not player.empty:
        id = player.iloc[0]['id']
        return id
    else:
        raise ValueError(f"This name is not in the database: {name}")
    
def name_id_for_website(name):
    player = player_elos[player_elos['name'] == name]
    if not player.empty:
        id = player.iloc[0]['id']
        return id
    else:
        return None
def id_stats(id):
    player = players_stats[players_stats['id'] == id]
    if not player.empty:
        player_hand = hand(player.iloc[0]['hand'])
        player_dob = date_to_unix(player.iloc[0]['dob'])
        player_height = player.iloc[0]['height']
        return [player_hand, player_dob, player_height]
    else:
        raise ValueError("Something went wrong!")

model = load_model(os.path.join(BASE_DIR,'tennis_betting_first_release.keras')) 
if __name__ == "__main__":
    player_1_name = input("First player name (ATP website names): ")
    player_2_name = input("Second player name (ATP website names): ")


        
    player_1_id = name_id(player_1_name)
    player_2_id = name_id(player_2_name)




    date = input("date YYYY/MM/DD example: 20060122: ")
    date = date_to_unix(date)

    series = input("Please input the series  (International, International Gold, ATP250, ATP500, Masters, Masters Cup, Masters 1000, Grand Slam: ")
    series = Series(series)

    court = input("Please input the court (Indoor/Outdoor): ")
    court = Court(court)

    surface = input("Please input the surface: ")
    surface=surface_func(surface)
    round = int(input("Please input the round: "))

    player_features = []
    player_features.extend([date, series, court, flatten_list(surface), round])

    player_features.extend(id_stats(player_1_id))
    player_features.extend(id_stats(player_2_id))
    surfaces = ["hard", "clay", "grass", "carpet"]
    for surface in surfaces:
        player1_row = player_elos[player_elos['id'] == player_1_id]
        player2_row = player_elos[player_elos['id'] == player_2_id]

        player1_val = player1_row[f"elo_{surface}"].iloc[0]
        player2_val = player2_row[f"elo_{surface}"].iloc[0]
        player1_matches = player1_row[f"matches_number_{surface}"].iloc[0]
        player2_matches = player2_row[f"matches_number_{surface}"].iloc[0]

        player_features.append(player1_val)
        player_features.append(player2_val)
        player_features.append(player1_matches)
        player_features.append(player2_matches)
    input = (flatten_list(player_features), match_history_for_main(player_1_id, date, round, 30, matches), match_history_for_main(player_2_id, date, round, 30, matches))
    input_1 = np.array([input[0]])    
    input_2 = np.array([input[1]])          
    input_3 = np.array([input[2]]) 


    prediction = model.predict((input_1, input_2, input_3))
    valoszinuseg = prediction[0][0]
    if valoszinuseg > 0.5:
        print(f"Predicted winner: {player_2_name}")
    else:
        print(f"Predicted winner: {player_1_name}")


def date_to_unix_website(x):
        try:
            date = datetime.strptime(str(x).replace("-",""), "%Y%m%d")
            return int(date.timestamp())
        except Exception as e:
            return -1

def prediction_for_website(player_1_name, player_2_name, date, series, court, surface, round):
    player_elos = pd.read_csv(os.path.join(BASE_DIR, "players_elo.csv"))
    matches = pd.read_csv(os.path.join(BASE_DIR, "matches.csv"))
        
    player_1_id = name_id_for_website(player_1_name)
    player_2_id = name_id_for_website(player_2_name)

    date = date_to_unix_website(date)
    series = Series(series)
    court = Court(court)
    surface=surface_func(surface)
    round = int(round)

    player_features = []
    player_features.extend([date, series, court, flatten_list(surface), round])    
    player_features.extend(id_stats(player_1_id))
    player_features.extend(id_stats(player_2_id))
    surfaces = ["hard", "clay", "grass", "carpet"]
    for surface in surfaces:
        player1_row = player_elos[player_elos['id'] == player_1_id]
        player2_row = player_elos[player_elos['id'] == player_2_id]

        player1_val = player1_row[f"elo_{surface}"].iloc[0]
        player2_val = player2_row[f"elo_{surface}"].iloc[0]
        player1_matches = player1_row[f"matches_number_{surface}"].iloc[0]
        player2_matches = player2_row[f"matches_number_{surface}"].iloc[0]

        player_features.append(player1_val)
        player_features.append(player2_val)
        player_features.append(player1_matches)
        player_features.append(player2_matches)
    input = (flatten_list(player_features), match_history_for_main(player_1_id, date, round, 30, matches), match_history_for_main(player_2_id, date, round, 30, matches))
    input_1 = np.array([input[0]])    
    input_2 = np.array([input[1]])          
    input_3 = np.array([input[2]]) 


    prediction = model.predict((input_1, input_2, input_3))
    valoszinuseg = prediction[0][0]
    if valoszinuseg > 0.5:
        return player_2_name
    else:
        return player_1_name
