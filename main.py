from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}

data = []

accessRanksOrTournaments = input("Você deseja acessar o rank de players ou algum torneio? (rank/torneio):")
if accessRanksOrTournaments == "rank":
    url = "https://www.hltv.org/stats/players?startDate=all&rankingFilter=Top30&minMapCount=50"
    req = Request(url, headers=headers)
    print("Requesting: " + url)
    html = urlopen(req)
    soup = BeautifulSoup(html, "html.parser")
    players = soup.find("table", {"class": "stats-table player-ratings-table"}).find("tbody").findAll("tr")
    for player in players:
        player_data = {
            "country": player.find("img", {"class": "flag"})["title"],
            "name": player.find("td", {"class": "playerCol"}).find("a").text,
            "teams": player.find("td", {"class": "teamCol"}).find("a").find("img")["title"],
            "maps": int(player.findAll("td", {"class": "statsDetail"})[0].text),
            "rounds": int(player.findAll("td", {"class": "statsDetail"})[1].text),
            "K/D Diff": int(player.find("td", {"class": "kdDiffCol"}).text),
            "K/D": float(player.findAll("td", {"class": "statsDetail"})[2].text),
            "Rating 1.0": float(player.find("td", {"class": "ratingCol"}).text),
        }
        data.append(player_data)
else:
    url = input("Insira a URL do torneio na HLTV (ex:https://www.hltv.org/events/7148/pgl-cs2-major-copenhagen-2024):")
    req = Request(url, headers=headers)
    print("Requesting: " + url)
    html = urlopen(req)
    soup = BeautifulSoup(html, "html.parser")
    tournament = soup.find("h1", {"class": "event-hub-title"}).text
    table = soup.findAll(id="GroupPlay")
    teams = table[0].findAll("table", {"class": "standard-box"})[0].findAll("tr")
    teams.pop(0)

    for team in teams:
        players_url = "https://www.hltv.org/" + team.find("div", {"class": "text-ellipsis"}).find("a")["href"]
        req = Request(players_url, headers=headers)
        print("Requesting: " + players_url)
        html = urlopen(req)
        soup = BeautifulSoup(html, "html.parser")
        players = soup.findAll("div", {"class": "playerFlagName"})
        players = [player.find("span", {"class": "text-ellipsis"}).text for player in players]

        team_data = {
            "name": team.find("div", {"class": "text-ellipsis"}).text.replace("\n", ""),
            "tournament": tournament,
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

df.to_csv("data.csv", index=False)

print(df.to_string(index=False))
