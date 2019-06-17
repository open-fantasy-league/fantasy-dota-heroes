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
    with open(os.getcwd() + '/../data/football_result_template.json') as f:
        match = json.load(f)

    series_info = json.load(urllib2.urlopen(urllib2.Request(
        "http://localhost/api/v1/results/leagues/" + str(DEFAULT_LEAGUE) + "/findByTeams",
        headers={'apiKey': FE_APIKEY, "Content-Type": "application/json"},
        data=json.dumps({'teamOne': match['teamOne'], 'teamTwo': match['teamTwo']})
    )))
    match_id = series_info[0]['matches'][0]['match']['matchId']
    series_id = series_info[0]['series']['seriesId']
    team_one_goals = match['teamOneGoals']
    team_two_goals = match['teamTwoGoals']
    pickees = []

    def appendPlayer(is_team_one, our_team_goals, other_team_goals):
        playing_mins = off - on
        closest_name = difflib.get_close_matches(name, [p['name'] for p in all_pickees], 1)[0]
        stats = []
        if conceded_whilst_playing(on, off, other_team_goals) == 0 and playing_mins >= 60:
            stats.append({'field': 'clean sheet', 'value': 1})
        stats.append({'field': 'goal conceded', 'value': conceded_whilst_playing(on, off, other_team_goals)})
        goals = len([g for g in our_team_goals if g['scorer'] == name])
        if goals:
            stats.append({'field': 'goal', 'value': goals})
        assists = len([g for g in our_team_goals if g['assist'] == name])
        if assists:
            stats.append({'field': 'assist', 'value': assists})
        stats.append({'field': 'playing', 'value': 1})
        if playing_mins >= 60:
            stats.append({'field': 'playing > 60 mins', 'value': 1})
        pickees.append({
            'id': next(p for p in all_pickees if p["name"] == closest_name)['id'],
            'isTeamOne': is_team_one, 'stats': stats
        })

    for name, on, off in match['teamOnePlayers']:
        appendPlayer(True, team_one_goals, team_two_goals)

    for name, on, off in match['teamTwoPlayers']:
        appendPlayer(False, team_two_goals, team_one_goals)


    data = json.dumps({
        'seriesId': series_id,
        'matches': [{
            'matchId': match_id,
            'teamOneMatchScore': len(team_one_goals),
            'teamTwoMatchScore': len(team_two_goals),
            'pickeeResults': pickees
        }]
    })
    try:
        req = urllib2.Request(API_LEAGUE_RESULTS_URL, data=data,
                              headers={'apiKey': FE_APIKEY, "Content-Type": "application/json"})
        response = urllib2.urlopen(req)
        print(response.read())
    except urllib2.HTTPError as e:
        print(e.read())


if __name__ == "__main__":
    add_game_manually()
