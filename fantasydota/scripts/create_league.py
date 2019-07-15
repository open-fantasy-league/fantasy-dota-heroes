import urllib2

import json

import os
from fantasydota.lib.constants import API_URL, DEFAULT_LEAGUE


def get_players(teams):
    pickees = []
    id = 0
    for team in teams:
        for player in team['players']:
            # player position and team name
            pickees.append({"id": id, "name": player[0], "value": 1.0, "limits": [player[1], team['name']]})
            id += 1
    return pickees


def create_league(name, tournament_id, url):
    filename = raw_input("players filename:")
    with open(os.getcwd() + "/../data/" + filename) as f:
        teams = json.load(f)

    FE_APIKEY = os.environ.get("FE_APIKEY")
    if not FE_APIKEY:
        print "Set your fantasy esport APIKEY environment variable"

    periods = []
    for day in ([15, 16, 17, 18, 20, 21, 22, 23, 24, 25]):
        if day < 20:
            multiplier = 1.0
        elif day < 25:
            multiplier = 2.0
        else:
            multiplier = 3.0
        periods.append({'start': '2019-08-{} 00:00'.format(day), 'end': '2019-08-{} 00:00'.format(day+1), 'multiplier': multiplier})

    data = {
        'name': name,
        'apiKey': FE_APIKEY,
        'tournamentId': tournament_id,
        'gameId': 1,
        'pickeeDescription': 'Player',
        'periodDescription': 'Daily',
        'startingMoney': 50.0,
        'teamSize': 5,
        'transferInfo': {
            'isCardSystem': True,
            'cardPackSize': 6,
            'cardPackCost': 5,
            'recycleValue': 0.2,
            'predictionWinMoney': 2.0
        },
        "periods": periods,
        "url": url,
        "applyPointsAtStartTime": True,
        "limits": [{'name': 'position', 'types': [
            {'name': 'Core', 'max': 2}, {'name': 'Support', 'max': 2}, {'name': 'Offlane', 'max': 1},
        ]},
                   {'name': 'team', 'max': 2, 'types': [{'name': t['name']} for t in teams]}
                   ],
        "stats": [
            {'name': 'kills', 'allFactionPoints': 0.3},
            {'name': 'deaths', 'allFactionPoints': -0.3},
            {'name': 'last hits', 'allFactionPoints': 0.003},
            {'name': 'denies', 'allFactionPoints': 0.003},
            {'name': 'GPM', 'description': 'Gold per Minute', 'allFactionPoints': 0.002},
            {'name': 'tower kills', 'allFactionPoints': 1.0},
            {'name': 'roshan kills', 'allFactionPoints': 1.0},
            {'name': 'teamfight participation', 'allFactionPoints': 3.0},
            {'name': 'observer wards', 'allFactionPoints': 0.25},
            {'name': 'dewards', 'allFactionPoints': 0.25},
            {'name': 'camps stacked', 'allFactionPoints': 0.5},
            {'name': 'runes', 'description':'runes picked up', 'allFactionPoints': 0.25},
            {'name': 'first blood', 'allFactionPoints': 4.0},
            {'name': 'stun seconds', 'allFactionPoints': 0.05},
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
    try:
        req = urllib2.Request(
            API_URL + "leagues/" + str(DEFAULT_LEAGUE), data=json.dumps({'transferOpen': True}), headers={
                "Content-Type": "application/json",
                "apiKey": FE_APIKEY
            }
        )
        response = urllib2.urlopen(req)
        print(response.read())
    except urllib2.HTTPError as e:
        print(e.read())
    # for fixture in fixtures:
    #     try:
    #         req = urllib2.Request(
    #             API_URL + "results/leagues/" + str(DEFAULT_LEAGUE),
    #             data=json.dumps(fixture), headers={
    #                 "Content-Type": "application/json",
    #                 "apiKey": FE_APIKEY
    #             }
    #         )
    #         response = urllib2.urlopen(req)
    #         print(response.read())
    #     except urllib2.HTTPError as e:
    #         print(e.read())

    # req = urllib2.Request(
    #     API_URL + "leagues/1/startPeriod", data=json.dumps(data), headers={
    #         'User-Agent': 'ubuntu:fantasydotaheroes:v1.0.0 (by /u/LePianoDentist)',
    #         "Content-Type": "application/json"
    #     }
    # )
    # response = urllib2.urlopen(req)
    # print(response.read())


if __name__ == "__main__":
    create_league("The International 2019", 10749, "https://liquipedia.net/dota2/The_International/2019")
