import csv
import re

input_file = "real_afl_attendance_2024.txt"
output_file = "parsed_real_afl_attendance_2024.csv"

def is_match_line(line):
    return re.match(r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)", line.strip())

def is_round_line(line):
    return re.match(r"^Round \d+", line.strip())

def is_bye_line(line):
    return "BYE" in line

with open(input_file, "r") as fin, open(output_file, "w", newline="") as fout:
    writer = csv.writer(fout)
    writer.writerow(["Round", "Date", "Home v Away Teams", "Venue", "Crowd", "Result", "Disposals", "Goals"])
    
    round_num = ""
    buffer = []
    for line in fin:
        line = line.rstrip("\n")
        if is_round_line(line):
            round_num = re.findall(r"\d+", line)[0]
            continue
        if not line.strip():
            continue
        if line.startswith("Date") and "Home v Away" in line:
            continue
        if is_bye_line(line):
            fields = [f.strip() for f in re.split(r"\s{2,}|\t", line)]
            writer.writerow([round_num] + fields[:7])
            continue
        if is_match_line(line):
            if buffer:
                writer.writerow(buffer)
                buffer = []
            fields = [f.strip() for f in re.split(r"\s{2,}|\t", line)]
            while len(fields) < 7:
                fields.append("")
            buffer = [round_num] + fields
            continue
        # Player stats lines
        if buffer:
            if buffer[-1]:
                buffer[-1] += "; " + line.strip()
            else:
                buffer[-1] = line.strip()
    if buffer:
        writer.writerow(buffer)