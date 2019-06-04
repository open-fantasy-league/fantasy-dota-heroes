import urllib2

import json

import os
from fantasydota.lib.herodict import herodict
from fantasydota.lib.calibration import calibrate_all_hero_values, squeeze_values_together
from fantasydota.lib.constants import API_URL, DEFAULT_LEAGUE


def get_fixtures():
    with open("fixtures.json") as f:
        j = json.load(f)
        fixtures = j['fixtures']
    matches = []
    periods = []
    for i, match in enumerate(fixtures):
        matches.append({
            'matchId': i, 'tournamentId': 1, 'teamOne': match[0], 'teamTwo': match[1],
            "startTstamp": match[2] + ":00"
        })
    period_starts = j['period_starts']
    for i, tstamp in period_starts:
        if i != 37:
            periods.append({'start': tstamp, 'end': period_starts, 'multiplier': 1.0})
        else:
            periods.append({'start': tstamp, 'end': '3000-12-05 15:00', 'multiplier': 2.0})
    return matches, periods


def get_players(teams):
    pickees = []
    id = 0
    for team in teams:
        for player in team[1]:
            # player position and team name
            pickees.append({"id": id, "name": player[0], "value": 1.0, "limits": [player[1], team[0]]})
            id += 1
    return pickees

def create_league(name, tournament_id, url):
    with open('players.json') as f:
        teams = json.load(f)

    FE_APIKEY = os.environ.get("FE_APIKEY")
    if not FE_APIKEY:
        print "Set your fantasy esport APIKEY environment variable"
    fixtures, periods = get_fixtures()

    data = {
        'name': name,
        'apiKey': FE_APIKEY,
        'tournamentId': tournament_id,
        'gameId': 3,
        'pickeeDescription': 'Player',
        'periodDescription': 'Week',
        'startingMoney': 0.0,
        'teamSize': 11,
        'transferInfo': {
            'cardSystem': True,

            # "transferDelayMinutes": 60,
            # "noWildcardForLateRegister": True,
            #'transferLimit': 5
        },
        "periods": periods,
        "url": url,
        "applyPointsAtStartTime": False,
        "limits": [{'name': 'position', 'types': [
            {'name': 'goalkeeper', 'max': 1}, {'name': 'defender', 'max': 4}, {'name': 'midfielder', 'max': 4},
            {'name': 'forward', 'max': 2}
        ]},
                   {'name': 'club', 'max': 2, 'types': [{'name': t[0]} for t in teams]}
                   ],
        "stats": [
            {'name': 'playing', 'allFactionPoints': 1.0},
            {'name': 'playing > 60 mins', 'allFactionPoints': 1.0},  # total 2 points when playing point added
            {'name': 'assist', 'allFactionPoints': 4.0},
            {'name': 'clean sheet', 'separateFactionPoints': [  # when on pitch, and must be 60+ mins
                {'name': 'goalkeeper', 'value': 5.0},
                {'name': 'defender', 'value': 4.0},
                {'name': 'midfielder', 'value': 1.0}
            ]},
             {'name': 'goal', 'separateFactionPoints': [
                 {'name': 'forward', 'value': 4.0},
                 {'name': 'defender', 'value': 7.0},
                 {'name': 'midfielder', 'value': 5.0}
             ]},
            {'name': 'goal conceded', 'separateFactionPoints': [
                 {'name': 'goalkeeper', 'value': -1.0},
                 {'name': 'defender', 'value': -1.0},
                 {'name': 'midfielder', 'value': -0.5}
             ]},
            {'name': 'shot saved', 'separateFactionPoints': [
                {'name': 'goalkeeper', 'value': 0.2},
            ]},
            {'name': 'penalty save', 'separateFactionPoints': [
                {'name': 'goalkeeper', 'value': 3.0},
            ]},
            {'name': 'yellow card', 'allFactionPoints': -1.0},
            {'name': 'red card', 'allFactionPoints': -2.0},
            {'name': 'own goal', 'allFactionPoints': -2.0},
            {'name': 'penalty miss', 'allFactionPoints': -3.0},
            {'name': 'WhoScored match rating (x % game played)', 'allFactionPoints': 1.0}
        ],
        'pickees': get_players(teams)
    }

    try:
        req = urllib2.Request(
            API_URL + "leagues/", data=json.dumps(data), headers={
                "Content-Type": "application/json"
            }
        )
        response = urllib2.urlopen(req)
        print(response.read())
    except urllib2.HTTPError as e:
        print(e.read())
    # try:
    #     req = urllib2.Request(
    #         API_URL + "leagues/" + str(DEFAULT_LEAGUE), data=json.dumps({'transferOpen': True, 'transferDelayMinutes': None}), headers={
    #             "Content-Type": "application/json",
    #             "apiKey": FE_APIKEY
    #         }
    #     )
    #     response = urllib2.urlopen(req)
    #     print(response.read())
    # except urllib2.HTTPError as e:
    #     print(e.read())

    for fixture in fixtures:
        try:
            req = urllib2.Request(
                API_URL + "results/leagues/" + str(DEFAULT_LEAGUE) + "/fixture",
                data=json.dumps(fixture), headers={
                    "Content-Type": "application/json",
                    "apiKey": FE_APIKEY
                }
            )
            response = urllib2.urlopen(req)
            print(response.read())
        except urllib2.HTTPError as e:
            print(e.read())

    # req = urllib2.Request(
    #     API_URL + "leagues/1/startPeriod", data=json.dumps(data), headers={
    #         'User-Agent': 'ubuntu:fantasydotaheroes:v1.0.0 (by /u/LePianoDentist)',
    #         "Content-Type": "application/json"
    #     }
    # )
    # response = urllib2.urlopen(req)
    # print(response.read())


if __name__ == "__main__":
    create_league("Premier League", 1, "https://liquipedia.net/dota2/Dota_Pit_League/Season_7")
