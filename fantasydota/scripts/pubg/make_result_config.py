from fantasydota.lib.pubg_players import pubg_init, pubg_beat_init


def make_result_config():
    out = []
    out_string = "results_config = [\n"
    teams = []
    current_team = {}
    for player in pubg_beat_init:
        if player['team'] not in teams:
            if current_team:
                out.append(current_team)
            current_team = {'team': player['team'], 'players': [], 'position': 101}
            teams.append(player['team'])
        current_team['players'].append({'name': player['name'], 'kills': 0})

    for team in out:
        out_string += "{'team': '%s', 'position': %s, 'players': [\n" % (team['team'], team['position'])
        for player in team['players']:
            out_string += "{'name': '%s', 'kills': %s},\n" % (player['name'], player['kills'])
        out_string += "]},\n"
    out_string += "]\n"
    with open("/home/jdog/projects/fantasy-dota-heroes/fantasydota/lib/pubg_results_auto.py", 'w+') as f:
        f.write(out_string)


if __name__ == "__main__":
    make_result_config()
