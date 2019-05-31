import datetime

import difflib
import json
import os
import sys

import re
import urllib2

from fantasydota.lib.constants import DEFAULT_LEAGUE
from fantasydota.scripts.get_dota_results import API_LEAGUE_RESULTS_URL


def conceded_whilst_playing(on, off, other_team_goals):
    return len([g for g in other_team_goals if on <= g["min"] <= off])


def add_game_manually():
    all_pickees = json.load(urllib2.urlopen(urllib2.Request("http://localhost/api/v1/pickees/" + str(DEFAULT_LEAGUE))))
    FE_APIKEY = os.environ.get("FE_APIKEY")
    if not FE_APIKEY:
        print "Set your fantasy esport APIKEY environment variable"
        exit()
    with open('/../data/football_result_template.json') as f:
        match = json.load(f)

    match_id = json.load(urllib2.urlopen(urllib2.Request(
        "http://localhost/api/v1/results/leagues/" + str(DEFAULT_LEAGUE) + "/findByTeams",
        headers={'apiKey': FE_APIKEY, "Content-Type": "application/json"},
        data={'teamOne': match['teamOne'], 'teamTwo': match['teamTwo']}
    )))[0]['matchId']
    team_one_goals = match['teamOneGoals']
    team_two_goals = match['teamTwoGoals']
    pickees = []
    for name, on, off in match['teamOnePlayers']:
        playing_mins = off - on
        closest_name = difflib.get_close_matches(name, [p['name'] for p in all_pickees], 1)[0]
        stats = []
        if conceded_whilst_playing(on, off, team_two_goals) == 0 and playing_mins >= 60:
            stats.append({'field': 'clean sheet', 'value': 1})
        stats.append({'field': 'conceded', 'value': conceded_whilst_playing})
        goals = len([g for g in team_one_goals if g['scorer'] == name])
        if goals:
            stats.append({'field': 'goals', 'value': goals})
        assists = len([g for g in team_one_goals if g['assists'] == name])
        if assists:
            stats.append({'field': 'assists', 'value': assists})
        pickees.append({
            'id': next(p for p in all_pickees if p["name"] == closest_name)['id'],
            'isTeamOne': True, 'stats': stats
        })


    # pickees = [{'id': all_pickees[0]['id'], 'isTeamOne': True, 'stats': [
    #     {'field': 'goal', 'value': 2}, {'field': 'WhoScored match rating', 'value': 8.6},{'field': 'clean sheet', 'value': 1}
    # ]}]
    data = json.dumps({
        'matchId': match_id,
        'teamOneScore': len(match['teamOneScore']),
        'teamTwoScore': len(match['teamTwoScore']),
        'tournamentId': 1,
        'pickees': pickees
    })
    # if team_one is not None:
    #     data['teamOne'] = team_one
    #     data['teamTwo'] = team_two
    try:
        req = urllib2.Request(API_LEAGUE_RESULTS_URL, data=data,
                              headers={'apiKey': FE_APIKEY, "Content-Type": "application/json"})
        response = urllib2.urlopen(req)
        print(response.read())
    except urllib2.HTTPError as e:
        print(e.read())


if __name__ == "__main__":
    add_game_manually()
