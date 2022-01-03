import csv
import os
import matplotlib.pyplot as plt
import numpy as np

total_h_goals, total_a_goals = 0, 0
h_wins, a_wins = 0, 0
month_goals, month_csheets = {}, {} # Key is month, value is value
Var = {}    # Keys are pre- / post-var, values are nested lists with related stats
teams = {}  # Nested dictionary with team stats as a dictionary as the value
refs = {}  # Nested dictionary with ref stats as a dictionary as the value - yellows, reds, fouls
current_year_refs = {}
home_refs, away_refs = [0, 0, 0], [0, 0, 0]     # Fouls, yellows, reds
total_games, home_cleansheets, away_cleansheets = 0, 0, 0

# Open and iterate through the files
for file in os.listdir("Season Stats"):
    file_name = os.path.join("Season Stats", file)
    if os.path.isfile(file_name):
        with open(file_name, "r") as f:
            csv_file = csv.DictReader(f)
            for line in csv_file:
                total_games += 1

                # Monthly goals data
                if line["Date"][5:7] not in month_goals:
                    month_goals[line["Date"][5:7]] = [int(line["FTHG"]) + int(line["FTAG"]), 1, int(line["FTHG"]) + int(line["FTAG"])]
                else:
                    month_goals[line["Date"][5:7]][0] += int(line["FTHG"]) + int(line["FTAG"])
                    month_goals[line["Date"][5:7]][1] += 1
                    month_goals[line["Date"][5:7]][2] = month_goals[line["Date"][5:7]][0]/month_goals[line["Date"][5:7]][1]

                # Simple data/prints - home goals percentage, home win percentage, home/away clean sheet percentage
                total_h_goals += int(line["FTHG"])
                total_a_goals += int(line["FTAG"])
                if line["FTR"] == "H":
                    h_wins += 1
                elif line["FTR"] == "A":
                    a_wins += 1
                if line["FTAG"] == "0":
                    home_cleansheets += 1
                if line["FTHG"] == "0":
                    away_cleansheets += 1

                # Home/Away Clean Sheet Graph Stats
                if line["Date"][5:7] not in month_csheets:
                    month_csheets[line["Date"][5:7]] = [[0, 0, 0], [0, 0, 0]]
                if line["FTAG"] == "0":
                    month_csheets[line["Date"][5:7]][0][0] += 1
                    month_csheets[line["Date"][5:7]][0][1] += 1
                    month_csheets[line["Date"][5:7]][0][2] = month_csheets[line["Date"][5:7]][0][0]/month_csheets[line["Date"][5:7]][0][1]
                else:
                    month_csheets[line["Date"][5:7]][0][1] += 1
                    month_csheets[line["Date"][5:7]][0][2] = month_csheets[line["Date"][5:7]][0][0]/month_csheets[line["Date"][5:7]][0][1]
                if line["FTHG"] == "0":
                    month_csheets[line["Date"][5:7]][1][0] += 1
                    month_csheets[line["Date"][5:7]][1][1] += 1
                    month_csheets[line["Date"][5:7]][1][2] = month_csheets[line["Date"][5:7]][1][0]/month_csheets[line["Date"][5:7]][1][1]
                else:
                    month_csheets[line["Date"][5:7]][1][1] += 1
                    month_csheets[line["Date"][5:7]][1][2] = month_csheets[line["Date"][5:7]][1][0]/month_csheets[line["Date"][5:7]][1][1]

                # VAR before/after
                if file == "seas-1819.csv" or file == "seas-1920.csv":
                    if "Pre-Var" not in Var:
                        Var["Pre-Var"] = [[0, 0, 0], [0, 0, 0]]
                    Var["Pre-Var"][0][0] += int(line["FTHG"]) + int(line["FTAG"])
                    Var["Pre-Var"][0][1] += 1
                    Var["Pre-Var"][1][0] += int(line["HR"]) + int(line["AR"])
                    Var["Pre-Var"][1][1] += 1
                elif file == "seas-2021.csv" or file == "seas-2122.csv":
                    if "Post-Var" not in Var:
                        Var["Post-Var"] = [[0, 0, 0], [0, 0, 0]]
                    Var["Post-Var"][0][0] += int(line["FTHG"]) + int(line["FTAG"])
                    Var["Post-Var"][0][1] += 1
                    Var["Post-Var"][1][0] += int(line["HR"]) + int(line["AR"])
                    Var["Post-Var"][1][1] += 1

                # Team dictionary stuff
                if line["HomeTeam"] not in teams:
                    teams[line["HomeTeam"]] = {"Goals": 0, "Wins": 0, "Games": 0}
                if line["AwayTeam"] not in teams:
                    teams[line["AwayTeam"]] = {"Goals": 0, "Wins": 0, "Games": 0}
                teams[line["HomeTeam"]]["Goals"] += int(line["FTHG"])
                teams[line["AwayTeam"]]["Goals"] += int(line["FTAG"])
                teams[line["HomeTeam"]]["Games"] += 1
                teams[line["AwayTeam"]]["Games"] += 1
                if line["FTR"] == "H":
                    teams[line["HomeTeam"]]["Wins"] += 1
                elif line["FTR"] == "A":
                    teams[line["AwayTeam"]]["Wins"] += 1

                # Ref dictionary stuff
                if file == "seas-2122.csv":
                    if line["Referee"] not in current_year_refs:
                        current_year_refs[line["Referee"]] = {"Name": line["Referee"], "Games": 0, "Yellows": 0, "Reds": 0, "Fouls": 0}
                    current_year_refs[line["Referee"]]["Games"] += 1
                    current_year_refs[line["Referee"]]["Yellows"] += int(line["HY"]) + int(line["AY"])
                    current_year_refs[line["Referee"]]["Reds"] += int(line["HR"]) + int(line["AR"])
                    current_year_refs[line["Referee"]]["Fouls"] += int(line["HF"]) + int(line["AF"])
                if line["Referee"] not in refs:
                    refs[line["Referee"]] = {"Games": 0, "Yellows": 0, "Reds": 0, "Fouls": 0}
                refs[line["Referee"]]["Games"] += 1
                refs[line["Referee"]]["Yellows"] += int(line["HY"]) + int(line["AY"])
                refs[line["Referee"]]["Reds"] += int(line["HR"]) + int(line["AR"])
                refs[line["Referee"]]["Fouls"] += int(line["HF"]) + int(line["AF"])

                # Fouls, yellows, reds totals
                home_refs[0] += int(line["HF"])
                away_refs[0] += int(line["AF"])
                home_refs[1] += int(line["HY"])
                away_refs[1] += int(line["AY"])
                home_refs[2] += int(line["HR"])
                away_refs[2] += int(line["AR"])

# Simple data/prints on various percentages
hg_percent = "Home Goals Percentage: {0:.2f}%."
print(hg_percent.format(total_h_goals/(total_h_goals+total_a_goals)*100))
h_win_percent = "Win percentage at home: {0:.2f}%."
print(h_win_percent.format(h_wins/(h_wins+a_wins)*100))
h_csheets = "Home clean sheet percentage: {0:.2f}%."
a_csheets = "Away clean sheet percentage: {0:.2f}%."
print(h_csheets.format(home_cleansheets/total_games*100))
print(a_csheets.format(away_cleansheets/total_games*100))

# Data/ graphs for monthly goals and clean sheets
goals_per_month = []
for lst in month_goals.values():
    goals_per_month.append(lst[2])
hcsheets_per_month, acsheets_per_month = [], []
for lst in month_csheets.values():
    hcsheets_per_month.append(lst[0][2])
    acsheets_per_month.append(lst[1][2])
plt.bar(month_goals.keys(), goals_per_month)
plt.ylim(2, 3)
plt.title("Goals Per Game in Each Month")
plt.xlabel("Months")
plt.ylabel("Goals Per Game")
plt.show()
n = 12
index = np.arange(n)
fig, ax = plt.subplots()
ax.bar(index, hcsheets_per_month, 0.4, color='r', label='Home')
ax.bar(index+0.4, acsheets_per_month, 0.4, color='b', label='Away')
ax.set_title("Home and Away Clean Sheet Percentage in Each Month")
ax.set_xlabel("Months")
ax.set_ylabel("Clean Sheet Percentage")
ax.set_xticks(index + 0.4 / 2)
ax.set_xticklabels(month_csheets.keys())
ax.legend()
plt.show()

# Data/graphs for pre- / post-var goals and red cards
Var["Pre-Var"][0][2] = Var["Pre-Var"][0][0] / Var["Pre-Var"][0][1]
Var["Post-Var"][0][2] = Var["Post-Var"][0][0] / Var["Post-Var"][0][1]
Var["Pre-Var"][1][2] = Var["Pre-Var"][1][0] / Var["Pre-Var"][1][1]
Var["Post-Var"][1][2] = Var["Post-Var"][1][0] / Var["Post-Var"][1][1]
goals, red_cards = [], []
for lst in Var.values():
    goals.append(lst[0][2])
    red_cards.append(lst[1][2])
plt.bar(Var.keys(), goals)
plt.ylim(2, 3)
plt.title("Goals Pre-Var vs Post-Var")
plt.xlabel("Pre-Var vs Post-Var")
plt.ylabel("Per Game Ratio")
plt.show()
plt.bar(Var.keys(), red_cards)
plt.ylim(0, 0.5)
plt.title("Red Cards Pre-Var vs Post-Var")
plt.xlabel("Pre-Var vs Post-Var")
plt.ylabel("Per Game Ratio")
plt.show()

# Data/graph for total team stats
sorted_tuples = sorted(teams.items(), key=lambda x: (x[1]["Games"], x[1]["Wins"], x[1]["Goals"]), reverse=True)
sorted_teams = {k: v for k, v in sorted_tuples}
team_goals, team_wins, team_games = [], [], []
for lst in sorted_teams.values():
    team_goals.append(lst["Goals"])
    team_wins.append(lst["Wins"])
    team_games.append(lst["Games"])
plt.bar(sorted_teams.keys(), team_goals, label="Goals")
plt.bar(sorted_teams.keys(), team_games, label="Games")
plt.bar(sorted_teams.keys(), team_wins, label="Wins")
plt.xlabel("Teams")
plt.ylabel("Totals")
plt.title("PL Team Stats: 2005-2021")
plt.xticks(rotation=90)
plt.legend()
plt.show()

# Data/Graph for total ref stats
sorted_tuples = sorted(refs.items(), key=lambda x: (x[1]["Games"], x[1]["Fouls"], x[1]["Yellows"], x[1]["Reds"]), reverse=True)
sorted_refs = {k: v for k, v in sorted_tuples}
ref_games, ref_fouls, ref_yellows, ref_reds = [], [], [], []
for lst in sorted_refs.values():
    ref_games.append(lst["Games"])
    ref_fouls.append(lst["Fouls"]/lst["Games"])
    ref_reds.append(lst["Reds"]/lst["Games"])
    ref_yellows.append(lst["Yellows"]/lst["Games"])
plt.bar(sorted_refs.keys(), ref_games, label="Games")
plt.bar(sorted_refs.keys(), ref_fouls, label="Fouls")
plt.bar(sorted_refs.keys(), ref_yellows, label="Yellows")
plt.bar(sorted_refs.keys(), ref_reds, label="Reds")
plt.title("Referee Stat Totals")
plt.xlabel("Referees")
plt.xticks(rotation=90)
plt.ylabel("Totals")
plt.legend()
plt.show()

# Data/graph for current year ref stats
sorted_tuples = sorted(current_year_refs.items(), key=lambda x: (x[1]["Games"], x[1]["Fouls"], x[1]["Yellows"], x[1]["Reds"]), reverse=True)
sorted_refs = {k: v for k, v in sorted_tuples}
current_ref_games, current_ref_fouls, current_ref_yellows, current_ref_reds = [], [], [], []
for lst in sorted_refs.values():
    current_ref_games.append(lst["Games"])
    current_ref_fouls.append(lst["Fouls"]/lst["Games"])
    current_ref_reds.append(lst["Reds"]/lst["Games"])
    current_ref_yellows.append(lst["Yellows"]/lst["Games"])
plt.bar(sorted_refs.keys(), current_ref_fouls, label="Fouls")
plt.bar(sorted_refs.keys(), current_ref_games, label="Games")
plt.bar(sorted_refs.keys(), current_ref_yellows, label="Yellows")
plt.bar(sorted_refs.keys(), current_ref_reds, label="Reds")
plt.title("Referee Stat Totals for Current 2021/2022 Season")
plt.xlabel("Referees")
plt.xticks(rotation=90)
plt.ylabel("Totals")
plt.legend()
plt.show()

# Data/Graph for home vs away ref stats
home_refs[0] = home_refs[0]/total_games
home_refs[1] = home_refs[1]/total_games
home_refs[2] = home_refs[2]/total_games
away_refs[0] = away_refs[0]/total_games
away_refs[1] = away_refs[1]/total_games
away_refs[2] = away_refs[2]/total_games
n = 3
index = np.arange(n)
fig, ax = plt.subplots()
ax.bar(index, home_refs, 0.4, color='r', label='Home')
ax.bar(index+0.4, away_refs, 0.4, color='b', label='Away')
ax.set_title("Ref Stats, Home vs Away")
ax.set_xlabel("Stats")
ax.set_ylabel("Per Game Ratio")
ax.set_xticks(index + 0.4 / 2)
ax.set_xticklabels(["Fouls", "Yellows", "Reds"])
ax.legend()
plt.show()
