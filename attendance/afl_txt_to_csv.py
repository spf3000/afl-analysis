import csv
import re

input_file = "data/real_afl_attendance_2021.txt"
output_file = "data/parsed_real_afl_attendance_2021.csv"

def is_match_line(line):
    return re.match(r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)", line.strip())

def is_round_line(line):
    return re.match(r"^Round \d+", line.strip())

def is_bye_line(line):
    return "BYE" in line

with open(input_file, "r") as fin, open(output_file, "w", newline="") as fout:
    writer = csv.writer(fout)
    writer.writerow(["Round", "Date", "Home v Away Teams", "Venue", "Crowd", "Result", "Disposals", "Goals"])
    reader = csv.reader(fin, delimiter="\t")
    round_num = ""
    buffer = []
    for line in reader:
        line_string =''.join(map(str, line)) 
        if is_round_line(line_string):
            round_num = re.findall(r"\d+", line_string)[0]
            continue
        if not line_string.strip():
            continue
        if line_string.startswith("Date") and "Home v Away" in line:
            continue
        if is_bye_line(line_string):
            fields = [f.strip() for f in  line]
            writer.writerow([round_num] + fields[:7])
            continue
        if is_match_line(line_string):
            if buffer:
                writer.writerow(buffer)
                buffer = []
            fields = [f.strip() for f in line]
            while len(fields) < 7:
                fields.append("")
            buffer = [round_num] + fields
            continue
        # Player stats lines
        if buffer:
            if buffer[-1]:
                buffer[-1] += "; " + line_string.strip()
            else:
                buffer[-1] = line_string.strip()
    if buffer:
        writer.writerow(buffer)