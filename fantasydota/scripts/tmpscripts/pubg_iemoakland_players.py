import re


def get_players():
    with open("../../junk/iemoakland.html") as f:
        html = f.read()
    output = []
    teams = re.findall('(?s)<div class="influencer-card">(.*?)<!-- Card End  -->', html)
    counter = 1
    for t in teams:
        team_name = re.search('<h1 class="influencer-name">([^<]+)</h1>', t).group(1)
        player_section = re.search('(?s)<p class="influencer-description">(.*?)</p>', t).group(1)
        players = re.findall('(?:<a[^>]+>)?\s*(.*?)(?:</a>)?<br />', player_section)
        if len(players) < 4:
            print(team_name)
            print(players)
        for player in players:
            if '<a hre' in player:
                player = re.search('<a[^>]+>([^<]+)', player).group(1)
            output.append({"id": counter, "name": player, "team": team_name, "value": 10.0})
            counter += 1

    with open("../../lib/pubg_players.py", "w+") as f:
        f.write("pubg_init = " + repr(output))
    return

if __name__ == "__main__":
    get_players()
