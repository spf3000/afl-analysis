import re
import csv

input_file = "data/ladder.txt"
output_file = "data/ladder.csv"


def is_round_line(line):
    return line.startswith("Rd")

team_names = {
    "GW":"GWS",
    "SY":"Sydney",
    "NM":"North Melbourne",
    "WB":"Western Bulldogs",
    "GC":"Gold Coast",
    "PA":"Port Adelaide",
    "HW":"Hawthorn",
    "SK":"St Kilda",
    "GE":"Geelong",
    "CW":"Collingwood",
    "ES":"Essendon",
    "CA":"Carlton",
    "RI":"Richmond",
    "AD":"Adelaide",
    "FR":"Fremantle",
    "WC":"West Coast",
    "BL":"Brisbane",
    "ME":"Melbourne",
}

with open(input_file, "r") as fin, open(output_file, "w", newline="") as fout:
    writer = csv.writer(fout)
    writer.writerow(["Year","Round", "Position", "Team", "Played", "Premiership_Points", "Percentage"])
    
    position = 1
    round_num = ""
    for line in fin:
        line = line.strip()
        if is_round_line(line):
            position = 1
            round_num = line.split()[1]  # Extract the round number
            continue
        if not line:
            continue  # Skip empty lines
        
        fields = [f.strip() for f in re.split(r"\s{2,}|\t", line)]
        if len(fields) == 4:
            fields[0] = team_names.get(fields[0], fields[0])  # Replace team code with full name
            writer.writerow([round_num, position] + fields)
            position += 1
