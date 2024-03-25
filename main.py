from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd

Team = {
    "name": "",
    "players": [],
    "roundsWon": 0,
    "roundsLost": 0,
    "result": "",
    "matches": []
}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "Referer": "https://www.google.com/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}

url = input("Insira a URL do torneio na HLTV (ex:https://www.hltv.org/events/7148/pgl-cs2-major-copenhagen-2024): ")
req = Request(url, headers=headers)
html = urlopen(req)
soup = BeautifulSoup(html, "html.parser")
table = soup.findAll(id="GroupPlay")
teams = table[0].findAll("table", {"class": "standard-box"})[0].findAll("tr")
teams.pop(0)

data = []

for team in teams:
    players_url = "https://www.hltv.org/" + team.find("div", {"class": "text-ellipsis"}).find("a")["href"]
    req = Request(players_url, headers=headers)
    html = urlopen(req)
    soup = BeautifulSoup(html, "html.parser")
    players = soup.findAll("div", {"class": "playerFlagName"})
    players = [player.find("span", {"class": "text-ellipsis"}).text for player in players]

    team_data = {
        "name": team.find("div", {"class": "text-ellipsis"}).text.replace("\n", ""),
        "players": players,
        "roundsWon": int(team.find("div", {"class": "cell-width-rw"}).text),
        "roundsLost": int(team.find("div", {"class": "cell-width-rl"}).text),
        "result": team.find("div", {"class": "cell-width-record"}).text,
        "matches": []
    }
    matches = team.findAll("a", {"class": "bottom-row"})
    for match in matches:
        team1 = match.findAll("span", {"class": "text-ellipsis"})[0].text
        team2 = match.findAll("span", {"class": "text-ellipsis"})[1].text
        resultLeft = match.find("div", {"class": "score-left"}).text
        resultRight = match.find("div", {"class": "score-right"}).text
        match_data = {
            "result": f"{team1} {resultLeft} - {resultRight} {team2}",
        }
        team_data["matches"].append(match_data)
    data.append(team_data)

df = pd.DataFrame(data)

print(df.to_string(index=False))
