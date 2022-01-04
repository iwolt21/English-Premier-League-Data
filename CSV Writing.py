import csv
import os

teams = {}  # Nested dictionary with team stats as a dictionary as the value
refs = {}  # Nested dictionary with ref stats as a dictionary as the value - yellows, reds, fouls
current_year_refs = {}
total_games = 0

# Open and iterate through the files
for file in os.listdir("Season Stats"):
    file_name = os.path.join("Season Stats", file)
    if os.path.isfile(file_name):
        with open(file_name, "r") as f:
            csv_file = csv.DictReader(f)
            for line in csv_file:
                total_games += 1

                # Team dictionary stuff
                if line["HomeTeam"] not in teams:
                    teams[line["HomeTeam"]] = {"Team": line["HomeTeam"], "Goals": 0, "Wins": 0, "Games": 0}
                if line["AwayTeam"] not in teams:
                    teams[line["AwayTeam"]] = {"Team": line["AwayTeam"], "Goals": 0, "Wins": 0, "Games": 0}
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
                    refs[line["Referee"]] = {"Name": line["Referee"], "Games": 0, "Yellows": 0, "Reds": 0, "Fouls": 0}
                refs[line["Referee"]]["Games"] += 1
                refs[line["Referee"]]["Yellows"] += int(line["HY"]) + int(line["AY"])
                refs[line["Referee"]]["Reds"] += int(line["HR"]) + int(line["AR"])
                refs[line["Referee"]]["Fouls"] += int(line["HF"]) + int(line["AF"])

ref_header = [key for key in refs["M Dean"].keys()]
with open('written_data_files/Ref_Stats.csv', "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=ref_header)
    writer.writeheader()
    writer.writerows(refs.values())

team_header = [key for key in teams["Brentford"].keys()]
with open("written_data_files/Team_Stats.csv", "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=team_header)
    writer.writeheader()
    writer.writerows(teams.values())

current_year_refs_header = [key for key in refs["M Dean"].keys()]
with open("written_data_files/current_ref_stats.csv", "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=current_year_refs_header)
    writer.writeheader()
    writer.writerows(current_year_refs.values())
