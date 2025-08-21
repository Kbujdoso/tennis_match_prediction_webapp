import os 
import json
import zipfile
import pandas as pd
import numpy as np
import math
from rapidfuzz import process, fuzz
from datetime import datetime
import re
import unicodedata
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
@staticmethod
def elo_calculator(Rating_A, played_matches_A, Rating_B,played_matches_B, result): #result True than A won result false than B won 
    Ka = max(32/math.sqrt(max(1, played_matches_A)/2),6)
    Kb = max(32/math.sqrt(max(1, played_matches_B)/2),6)
    Ea = 1 / (1 + 10 ** ((Rating_B-Rating_A)/400))
    Eb = 1-Ea
    if result:
        Rating_A_new = Rating_A + Ka * (1-Ea)
        Rating_B_new = Rating_B + Kb * (0-Eb)  
    else: 
        Rating_A_new = Rating_A + Ka * (0-Ea)
        Rating_B_new = Rating_B + Kb * (1-Eb)
    return (round(Rating_A_new, 1), round(Rating_B_new,1))
def clean_name(name):
    if pd.isnull(name):  
        return ""
    name = str(name)
    name = unicodedata.normalize("NFKC", name)
    name = re.sub(r"[-]", " ", name)         
    name = re.sub(r"\s+", " ", name)            
    name = name.strip()
    return name.replace(" ", "")

def score(x):
        sets = str(x).split()  
        result = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        helper = []
        for s in sets:
            games = s.split("-")
            for g in games:
                helper.append(int(g))
        for i in range(len(helper)):
            result[i] = helper[i]
        return result

def date_to_unix(x):
        x = str(x).replace("-", "")  
        date = datetime.strptime(str(x), "%Y%m%d")
        return int(date.timestamp())

def Court(x):
        if x == "Indoor":
            return [1,0]
        elif x == "Outdoor":
            return [0,1]
        else: 
            return -1

def Series(x):
        match x:
            case "International":
                return 0
            case "International Gold":
                return 1
            case "ATP250":
                return 2
            case "ATP500":
                return 3
            case "Masters":
                return 4
            case "Masters Cup":
                return 5
            case "Masters 1000":
                return 6
            case "Grand Slam":
                return 7
            case _:
                return -1
            
def Round(x):
    match x:
        case "1st Round":
            return 0
        case "2nd Round":
            return 1
        case "3rd Round":
            return 2
        case "4th Round":
            return 3
        case "Round Robin":
            return 4
        case "Quarterfinals":
            return 5
        case "Semifinals":
            return 6
        case "The Final":
            return 7
        case _:
            return -1

def surface_func(x):
    if x == "Hard":
        return "[1,0,0,0]"
    elif x == "Clay":
        return "[0,1,0,0]"
    elif x == "Grass": 
        return "[0,0,1,0]"
    elif x == "Carpet": 
        return "[0,0,0,1]"

def hand(x):
    if x == "R":
        return "[1,0]"
    if x == "L":
        return "[0,1]"
    else:
        return "[-1, -1]"

def flatten_list(x):
    result = []
    if isinstance(x, list):
        for i in range(len(x)):
            result.extend(flatten_list(x[i])) 
    else:
        result.append(x)
    return result
if __name__ =="__main__":
    def different_database_helper_not_needed_anymore():
        player_full_names = pd.read_csv(os.path.join(BASE_DIR, "full_name_players.csv"))
        full_name_player_matches = pd.read_csv("full_name_player_matches.csv")
        def date_to_unix_full_name(x):
            x = str(x).split(".")[0]
            try:   
                date = datetime.strptime(str(x), "%Y%m%d")
                return int(date.timestamp())
            except ValueError:
                return -1
        full_name_player_matches["tourney_date"] = full_name_player_matches["tourney_date"].apply(date_to_unix_full_name)
        full_name_player_matches = full_name_player_matches[full_name_player_matches["tourney_date"] > 946684860]
        """    level = ["G", "A", "M", "T"]
        full_name_player_matches = full_name_player_matches[full_name_player_matches["tourney_level"].isin(level)]"""
        player_full_names = player_full_names[
        (player_full_names["player_id"].isin(full_name_player_matches["winner_id"])) |
        (player_full_names["player_id"].isin(full_name_player_matches["loser_id"]))
                            ]

        player_full_names["full_name"] = player_full_names["name_last"] + " " + player_full_names["name_first"]
        full_names = player_full_names["full_name"].unique().tolist()

    kaggle_path = "./kaggle.json"

    with open (kaggle_path, "r") as f: 
        creds = json.load(f)

    os.environ["KAGGLE_USERNAME"] = creds["username"]
    os.environ["KAGGLE_KEY"] = creds["key"]
    filename = "atp_tennis.csv"
    os.system("kaggle datasets download -d dissfya/atp-tennis-2000-2023daily-pull")
    with zipfile.ZipFile("atp-tennis-2000-2023daily-pull.zip", 'r') as zip_ref:
        for member in zip_ref.namelist():
            filename = os.path.basename(member)
            if not filename:
                continue 
            with zip_ref.open(member) as source, open(filename, "wb") as target:
                target.write(source.read())
    zip_path = "atp-tennis-2000-2023daily-pull.zip"
    if os.path.exists(zip_path):
        os.remove(zip_path)



    columns = ["Date", "Series", "Court", "Surface", "Round", "Best of", "Player_1", "Player_2", "Winner", "Rank_1", "Rank_2", "Pts_1", "Pts_2", "Odd_1", "Odd_2", "Score"]
    matches = pd.read_csv("atp_tennis.csv")

    matches = matches[columns]





    matches["Date"] = matches["Date"].apply(date_to_unix)

    

    matches["Score"] = matches["Score"].apply(score)

    set_oszlopok = matches['Score'].apply(pd.Series)
    set_oszlopok.columns = [f'set_{i+1}' for i in range(set_oszlopok.shape[1])]
    matches = matches.drop(columns=['Score']) 
    matches = pd.concat([matches, set_oszlopok], axis=1)
    sets = [
    "set_1","set_2","set_3","set_4","set_5","set_6","set_7","set_8","set_9","set_10"
    ]
    matches[sets] = matches[sets].applymap(lambda x: int(x) if str(x).isdigit() else -1)

    
        
    matches["Court"] = matches["Court"].apply(Court)


    
            
    matches["Series"] = matches["Series"].apply(Series)



    matches["Round"] = matches["Round"].apply(Round)

    def rapidfuzz_matching_not_needed_anymore(full_names):
        names_player_1 = matches["Player_1"].unique().tolist()
        names_player_2 = matches["Player_2"].unique().tolist()
        names = names_player_1 + names_player_2
        for i in range(len(names)):
            names[i] = clean_name(names[i])
        names = list(set(names))
        names.sort()

        matched_names = []
        unmatched_names = []
        full_names.sort()
        matched_names_csv = pd.DataFrame(columns=["id", "short_name", "full_name"])

        for i in range(len(names)):
            result = process.extractOne(
                names[i],
                full_names,
                scorer=fuzz.ratio,
                score_cutoff=65
            )
            if result:  
                best_match, score, _ = result
                matched_names_csv.loc[i] = [i+1, names[i], best_match]
            else:
                unmatched_names.append(names[i])
        with open("matched_names.txt", "w", encoding="utf-8") as f:
            for i in matched_names:
                f.write("(" + i[0] + ", " + i[1] + ")" + "\n")
        matched_names_csv.to_csv("matched_names.csv")

        player_data = pd.DataFrame(columns = ["id","short_name", "full_name", "hand", "birth", "ioc", "height"])
        player_data = matched_names_csv.merge(player_full_names, on="full_name", how="left")
        player_data = player_data.drop(columns= ["ioc", "player_id", "name_first", "name_last", "wikidata_id"])
        player_data.to_csv("player_Data.csv", index=False)

        with open("unmatched_names.txt", "w", encoding="utf-8") as f:
            for i in unmatched_names:
                f.write(i + "\n")

    player_data_manual = pd.read_csv("player_features.csv")

    
    bad_names =[]

    name_id = {}
    for i in range(len(player_data_manual)):
        name_id.update({clean_name(player_data_manual.loc[i, "short_name"]) : player_data_manual.loc[i, "id"]})
    id_stats = {
        row["id"]: {
            "short_name": clean_name(row["short_name"]),
            "hand": row["hand"],
            "dob": row["dob"],
            "height": row["height"],
            "Hard": (1400,0),
            "Clay": (1400,0),
            "Grass": (1400,0),
            "Carpet": (1400,0)
        }
        for _, row in player_data_manual.iterrows()
    }

    def Player(x):
        id = name_id.get(clean_name(x))
        if id:
            return id
        else:
            bad_names.append(x)
    
    matches["Player_1"] = matches["Player_1"].apply(clean_name)
    matches["Player_2"] = matches["Player_2"].apply(clean_name)
    matches["Winner"] = matches["Winner"].apply(clean_name)
    matches["Player_1"] = matches["Player_1"].apply(Player)
    matches["Player_2"] = matches["Player_2"].apply(Player)
    matches["Winner"] = matches["Winner"].apply(Player)
    bad_names = list(set(bad_names))
    player_data_manual = pd.read_csv("player_features.csv")
    print(player_data_manual.columns.tolist())

    bad_names.sort()
    if bad_names != []:
        print(f"Please add the following players {bad_names}")
        for i in range(len(bad_names)):
            while True:
                print(f"Please for this short name {bad_names[i]} write fullname, hand, birth, height in this order")
                full_name = input("fullname: ")
                hand = input("hand (R/L): ")
                birth = input("birth YYYY/MM/DD example: 20060122: ")
                height = input("height in cm: ")

                self_check = input("Please check if all data is correct. If it is correct, write 'correct'. If not, press Enter: ")

                if self_check == "correct":
                    last_id = max(id_stats.keys())
                    new_id = last_id + 1
                    id_stats[new_id] = {
                        "hand": hand,
                        "dob": birth,
                        "height": height,
                        "Hard": (1400,0),
                        "Clay": (1400, 0),
                        "Grass": (1400,0),
                        "Carpet": (1400, 0),
                    }
                    name_id[clean_name(bad_names[i])] = new_id

                    new_line = {
                        "id": new_id,
                        "short_name": bad_names[i],
                        "full_name": full_name,
                        "hand": hand,
                        "dob": birth,
                        "height": height
                    }
                    player_data_manual = pd.concat([player_data_manual, pd.DataFrame([new_line])], ignore_index=True)
                    player_data_manual.to_csv("player_features.csv", index=False)

                    break

    surfaces = ["Hard", "Clay", "Grass", "Carpet"]


    for i in range(len(matches)):
        matches.loc[i, "Player_1_hand"] = id_stats.get(matches.loc[i, "Player_1"])["hand"]
        matches.loc[i, "Player_1_dob"] = id_stats.get(matches.loc[i, "Player_1"])["dob"]
        matches.loc[i, "Player_1_height"] = id_stats.get(matches.loc[i, "Player_1"])["height"]

        matches.loc[i, "Player_2_hand"] = id_stats.get(matches.loc[i, "Player_2"])["hand"]
        matches.loc[i, "Player_2_dob"] = id_stats.get(matches.loc[i, "Player_2"])["dob"]
        matches.loc[i, "Player_2_height"] = id_stats.get(matches.loc[i, "Player_2"])["height"]

        #setting the elo
        print(i)
        for surface in surfaces:
            surface_lower = surface.lower()
            matches.loc[i, f"Player_1_elo_{surface_lower}"] = id_stats.get(matches.loc[i,"Player_1"])[surface][0]
            matches.loc[i, f"Player_2_elo_{surface_lower}"] = id_stats.get(matches.loc[i,"Player_2"])[surface][0]
            matches.loc[i, f"Player_1_matches_{surface_lower}"] = id_stats.get(matches.loc[i,"Player_1"])[surface][1]
            matches.loc[i, f"Player_2_matches_{surface_lower}"] = id_stats.get(matches.loc[i,"Player_2"])[surface][1]

        winner_id = matches.loc[i, "Winner"]
        if matches.loc[i, "Winner"] == matches.loc[i, "Player_1"]:
            loser_id = matches.loc[i, "Player_2"]
            player_1 = True
        else:
            loser_id = matches.loc[i, "Player_1"]
            player_1 = False
        surface = matches.loc[i, "Surface"]
        winner_elo, winner_matches = id_stats.get(winner_id)[surface]
        loser_elo, loser_matches = id_stats.get(loser_id)[surface]

        winner_new_elo, loser_new_elo = elo_calculator(winner_elo, winner_matches, loser_elo, loser_matches, True)
        id_stats[winner_id][surface] = (winner_new_elo, winner_matches + 1)
        id_stats[loser_id][surface] = (loser_new_elo, loser_matches + 1)




    players = pd.DataFrame(columns=[
    "id", "name",
    "elo_hard", "elo_clay", "elo_grass", "elo_carpet",
    "matches_number_hard", "matches_number_clay", "matches_number_grass", "matches_number_carpet"
])


    matches["Surface"] = matches["Surface"].apply(surface_func)



    matches["Player_1_hand"] = matches["Player_1_hand"].apply(hand)
    matches["Player_2_hand"] = matches["Player_2_hand"].apply(hand)

    def date_to_unix(x):
            try:
                date = datetime.strptime(str(x).split(".")[0], "%Y%m%d")
                return int(date.timestamp())
            except Exception as e:
                return -1

    matches["Player_1_dob"] = matches["Player_1_dob"].apply(date_to_unix)
    matches["Player_2_dob"] = matches["Player_2_dob"].apply(date_to_unix)

    cutoff = 1120428000  

    matches = matches[matches["Date"] >= cutoff]

    matches.to_csv("matches.csv", index=False)



    for i in range(len(player_data_manual)):
        player_id = player_data_manual.loc[i, "id"]
        player_name = player_data_manual.loc[i, "full_name"]

        elo_hard, matches_hard = id_stats[player_id]["Hard"]
        elo_clay, matches_clay = id_stats[player_id]["Clay"]
        elo_grass, matches_grass = id_stats[player_id]["Grass"]
        elo_carpet, matches_carpet = id_stats[player_id]["Carpet"]

        players.loc[i] = [
            player_id,
            player_name,
            elo_hard,
            elo_clay,
            elo_grass,
            elo_carpet,
            matches_hard,
            matches_clay,
            matches_grass,
            matches_carpet
        ]


    players.to_csv("players_elo.csv", index=False) 





