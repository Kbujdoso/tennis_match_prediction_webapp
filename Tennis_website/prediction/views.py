import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from django.shortcuts import render
import markdown
import os 
from django.conf import settings
from Tennis_match_prediction.main import prediction_for_website, name_id_for_website
import csv
import json
from django.http import JsonResponse

from rapidfuzz import process


player_list = []
with open('/home/koppany/Tennis_website/Tennis_match_prediction/player_features.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        player_list.append(row[2])

def index(request):
    return render(request,"prediction/index.html")

def prediction(request):
    return render(request,"prediction/prediction.html")


def show_markdown(request):
    md_path = os.path.join(settings.BASE_DIR,".." ,"Tennis_match_prediction", "README.md")
    md_path = os.path.abspath(md_path)
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()
    html_content = markdown.markdown(text)
    return render(request, "prediction/index.html", {"content": html_content})

def prediction_view(request): 
    result = None
    if request.method == "POST": 
        player1 = request.POST.get("player1")
        player2 = request.POST.get("player2")
        if (name_id_for_website(player1) != None and name_id_for_website(player2) != None):
            date = request.POST.get("date")
            series = request.POST.get("series")
            court = request.POST.get("court")
            surface = request.POST.get("surface")
            round = request.POST.get("round")
            result = prediction_for_website(player1, player2, date, series, court, surface, round)

            return render(request, "prediction/prediction.html", {
                "result": result,
                "player_list_json": json.dumps(player_list)
            })
        else:
            return render(request, "prediction/prediction.html", {
                "result": "Invalid name please enter a valid name which is int the database.",
                "player_list_json": json.dumps(player_list)
            })
        
    
def levenshtein(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]
def autocomplete_player(request):
    query = request.GET.get('q', '')
    threshold = 10
    unique_players = list(dict.fromkeys(player_list))
    distances = [(player, levenshtein(player.lower(), query.lower())) for player in unique_players]
    filtered = [player for player, dist in distances if dist <= threshold]
    suggestions = sorted(filtered, key=lambda x: levenshtein(x.lower(), query.lower()))[:3]
    return JsonResponse({'suggestions': suggestions})

