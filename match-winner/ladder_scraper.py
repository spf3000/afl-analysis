import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# Replace with the year you're targeting
season_url = "https://afltables.com/afl/seas/2025.html"
response = requests.get(season_url)
soup = BeautifulSoup(response.content, "html.parser")

ladder_data = []

# Find all tables that mention "Ladder"
for table in soup.find_all("table", {"border": "1"}):
    header = table.find("td")
    if header and "Ladder" in header.text:
        round_text = header.text.strip()
        round_num = int(round_text.split()[1])

        row_index = 1
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            team_abbr = cols[0].text.strip()
            played = int(cols[1].text.strip())
            points = int(cols[2].text.strip())
            pct = float(cols[3].text.strip())

            ladder_data.append({
                "Round": round_num,
                "Position": row_index,
                "Team": team_abbr,
                "Played": played,
                "Premiership_Points": points,
                "Percentage": pct
            })
            row_index += 1

ladder_df = pd.DataFrame(ladder_data)
print(ladder_df.head(50))
output_file = "data/ladder_2025.csv"
ladder_df.to_csv(output_file, index=False)
