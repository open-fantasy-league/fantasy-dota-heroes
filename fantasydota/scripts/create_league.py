import urllib2

import json
from fantasydota.lib.herodict import herodict
from fantasydota.lib.calibration import calibrate_all_hero_values
from fantasydota.lib.constants import API_URL


def create_league(name, tournament_id, url):

    data = {
        'name': name,
        'apiKey': 'A',
        'tournamentId': tournament_id,
        'gameId': 1,
        'pickeeDescription': 'Hero',
        'periodDescription': 'Day',
        'transferLimit': 5,
        'transferWildcard': True,
        "transferBlockedDuringPeriod": True,
        "extraStats": ["wins", "picks", "bans"],
        "periods": [
            {"start": "2002-02-02 04:05", "end": "2002-02-02 04:05", "multiplier": 1},
            {"start": "2002-02-02 04:05", "end": "2002-02-02 04:05", "multiplier": 1},
            {"start": "2002-02-02 04:05", "end": "2002-02-02 04:05", "multiplier": 2.2}
        ],
        "url": url
    }
    pickees = []
    hero_values = calibrate_all_hero_values([10548, 9862, 10482, 10547, 10603, 10440, 10560], 0)
    for id, name in herodict.items():
        #pickees.append({"id": id, "name": name, "value": 9.0})#hero_values[id]})
        pickees.append({"id": id, "name": name, "value": hero_values[id]})
    data['pickees'] = pickees

    try:
        req = urllib2.Request(
            API_URL + "leagues/", data=json.dumps(data), headers={
                'User-Agent': 'ubuntu:fantasydotaheroes:v1.0.0 (by /u/LePianoDentist)',
                "Content-Type": "application/json"
            }
        )
        response = urllib2.urlopen(req)
        print(response.read())
    except urllib2.HTTPError as e:
        print(e.read())
    try:
        req = urllib2.Request(
            API_URL + "leagues/1", data=json.dumps({'transferOpen': True}), headers={
                'User-Agent': 'ubuntu:fantasydotaheroes:v1.0.0 (by /u/LePianoDentist)',
                "Content-Type": "application/json"
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
    create_league("TI8", 9870, "www.yeah")
