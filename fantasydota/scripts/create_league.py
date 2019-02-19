import urllib2

import json

import os
from fantasydota.lib.herodict import herodict
from fantasydota.lib.calibration import calibrate_all_hero_values
from fantasydota.lib.constants import API_URL, DEFAULT_LEAGUE


def create_league(name, tournament_id, url):

    FE_APIKEY = os.environ.get("FE_APIKEY")
    if not FE_APIKEY:
        print "Set your fantasy esport APIKEY environment variable"

    data = {
        'name': name,
        'apiKey': FE_APIKEY,
        'tournamentId': tournament_id,
        'gameId': 1,
        'pickeeDescription': 'Hero',
        'periodDescription': 'Day',
        'startingMoney': 50.0,
        'transferInfo': {
            'transferWildcard': True,
            "transferBlockedDuringPeriod": False,
            "transferDelayMinutes": 60,
            "noWildcardForLateRegister": True,
            'transferLimit': 5
        },
        "extraStats": ["wins", "picks", "bans"],
        "periods": [
            {"start": "2018-02-20 02:00", "end": "2018-02-20 16:00", "multiplier": 1},
            {"start": "2018-02-21 02:00", "end": "2018-02-21 16:00", "multiplier": 1},
            {"start": "2018-02-22 02:00", "end": "2018-02-22 15:00", "multiplier": 2},
            {"start": "2018-02-23 02:00", "end": "2018-02-23 16:00", "multiplier": 2},
            {"start": "2018-02-24 05:00", "end": "2018-02-24 15:00", "multiplier": 3}
        ],
        "url": url,
        "applyPointsAtStartTime": False
    }
    pickees = []
    katowice_calib = [10560, 10575, 10733, 10681, 10532]
    hero_values = calibrate_all_hero_values(katowice_calib, 1549241783)
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
            API_URL + "leagues/" + str(DEFAULT_LEAGUE), data=json.dumps({'transferOpen': True, 'transferDelayMinutes': 10}), headers={
                'User-Agent': 'ubuntu:fantasydotaheroes:v1.0.0 (by /u/LePianoDentist)',
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
    create_league("MDL Macau", 10560, "https://liquipedia.net/dota2/Mars_Dota_2_League/Macau/2019")
