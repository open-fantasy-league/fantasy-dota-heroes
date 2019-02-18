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
        'apiKey': '3c7bfa1b-3a75-49e9-ae64-f0c6b042c0db',
        'tournamentId': tournament_id,
        'gameId': 1,
        'pickeeDescription': 'Hero',
        'periodDescription': 'Day',
        'transferLimit': 5,
        'startingMoney': 50.0,
        'transferWildcard': True,
        "transferBlockedDuringPeriod": False,
        "transferDelayMinutes": 10,
        "extraStats": ["wins", "picks", "bans"],
        "periods": [
            {"start": "2002-02-18 03:00", "end": "2002-02-18 04:00", "multiplier": 1},
            {"start": "2002-02-18 04:30", "end": "2002-02-18 05:00", "multiplier": 1},
            {"start": "2002-02-02 04:05", "end": "2002-02-02 04:05", "multiplier": 2.2}
        ],
        "url": url
    }
    pickees = []
    # katowice_calib = [10560, 10575, 10733, 10681, 10532]
    # hero_values = calibrate_all_hero_values(katowice_calib, 1549241783)
    # for id, name in herodict.items():
    #     #pickees.append({"id": id, "name": name, "value": 9.0})#hero_values[id]})
    #     pickees.append({"id": id, "name": name, "value": hero_values[id]})
    # data['pickees'] = pickees
    #
    # try:
    #     req = urllib2.Request(
    #         API_URL + "leagues/", data=json.dumps(data), headers={
    #             'User-Agent': 'ubuntu:fantasydotaheroes:v1.0.0 (by /u/LePianoDentist)',
    #             "Content-Type": "application/json"
    #         }
    #     )
    #     response = urllib2.urlopen(req)
    #     print(response.read())
    # except urllib2.HTTPError as e:
    #     print(e.read())
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
    create_league("ESL Katowice", 10424, "https://liquipedia.net/dota2/ESL_One/Katowice/2019")
