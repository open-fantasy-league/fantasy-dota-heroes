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
    print(on, off, other_team_goals)
    return len([g for g in other_team_goals if on <= g["min"] <= off])


def add_game_manually():
    with open(os.getcwd() + '/../data/football_result_template.json') as f:
        match = json.load(f)
    add_game(match)


def add_game(match):
    all_pickees = json.load(urllib2.urlopen(urllib2.Request("http://localhost/api/v1/pickees/" + str(DEFAULT_LEAGUE))))
    FE_APIKEY = os.environ.get("FE_APIKEY")
    if not FE_APIKEY:
        print "Set your fantasy esport APIKEY environment variable"
        exit()

    series_info = json.load(urllib2.urlopen(urllib2.Request(
        "http://localhost/api/v1/results/leagues/" + str(DEFAULT_LEAGUE) + "/findByTeams",
        headers={'apiKey': FE_APIKEY, "Content-Type": "application/json"},
        data=json.dumps({'teamOne': match['teamOne'], 'teamTwo': match['teamTwo']})
    )))
    match_id = series_info[0]['matches'][0]['match']['matchId']
    series_id = series_info[0]['series']['seriesId']
    team_one_goals = match['teamOneGoals']
    team_two_goals = match['teamTwoGoals']
    team_one_penalty_miss = match['penaltyMiss']['teamOne']
    team_two_penalty_miss = match['penaltyMiss']['teamTwo']
    own_goals = match['ownGoals']
    red_cards = match['redCards']
    pickees = []

    all_goals = match['teamOneGoals'] + match['teamTwoGoals']
    players = match['teamOnePlayers'] + match['teamTwoPlayers']
    unsung_players = [p for p in players if p[0] not in ([x['scorer'] for x in all_goals] + [x['assist'] for x in all_goals])]
    unsung_players.sort(key=lambda p: p[3], reverse=True)
    unsung_players = [p[0] for p in unsung_players][:3]
    highest_off = max(x[2] for x in match['teamOnePlayers'])

    def appendPlayer(name, on, off, is_team_one, our_team_goals, other_team_goals, red_cards):
        red_cards = [x for x in red_cards if x[0] == name]
        playing_mins = off - on if len(red_cards) < 1 else red_cards[0][1] - on
        closest_name = name #difflib.get_close_matches(name, [p['name'] for p in all_pickees], 1)[0]
        pickee = next(p for p in all_pickees if p["name"] == closest_name)
        is_keeper = pickee['limitTypes']['position'] == 'Goalkeeper'
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
        yellow_cards = len([x for x in match['yellowCards'] if x == name])
        if yellow_cards:
            stats.append({'field': 'yellow card', 'value': 1})
        if red_cards:
            stats.append({'field': 'red card', 'value': 1})
        if name in unsung_players:
            stats.append({'field': 'unsung hero (fotmob rating)', 'value': 5 - unsung_players.index(name)})

        if is_keeper and is_team_one:
            saved = int(raw_input("team one saves on/off: {}:{}".format(on, off))) if on != 0 or off != highest_off else match['teamOneSaves']
            stats.append({'field': 'shot saved', 'value': saved})
            if len(team_two_penalty_miss):
                stats.append({
                    'field': 'penalty save',
                    'value': len([p for p in team_two_penalty_miss if on <= p[1] < off])
                })
        if is_keeper and not is_team_one:
            saved = int(raw_input("team one saves on/off: {}:{}".format(on, off))) if on != 0 or off != highest_off else match['teamTwoSaves']

            stats.append({'field': 'shot saved', 'value': saved})
            if len(team_one_penalty_miss):
                stats.append({
                    'field': 'penalty save',
                    'value': len([p for p in team_one_penalty_miss if on <= p[1] < off])
                })
        num_own_goals = len([x for x in own_goals if x == name])
        if num_own_goals:
            stats.append({
                'field': 'own goal',
                'value': num_own_goals
            })
        pickees.append({
            'id': pickee['id'],
            'isTeamOne': is_team_one, 'stats': stats
        })

    for name, on, off, rating in match['teamOnePlayers']:
        appendPlayer(name, on, off, True, team_one_goals, team_two_goals, red_cards)

    for name, on, off, rating in match['teamTwoPlayers']:
        appendPlayer(name, on, off, False, team_two_goals, team_one_goals, red_cards)

    data = json.dumps({
        'seriesId': series_id,
        'matches': [{
            'matchId': match_id,
            'teamOneMatchScore': len(team_one_goals),
            'teamTwoMatchScore': len(team_two_goals),
            'pickeeResults': pickees
        }]
    })
    print(data)
    try:
        req = urllib2.Request(API_LEAGUE_RESULTS_URL, data=data,
                              headers={'apiKey': FE_APIKEY, "Content-Type": "application/json"})
        response = urllib2.urlopen(req)
        print(response.read())
    except urllib2.HTTPError as e:
        print(e.read())


if __name__ == "__main__":
    add_game_manually()
