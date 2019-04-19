import urllib2

import json

import os
from fantasydota.lib.herodict import herodict
from fantasydota.lib.calibration import calibrate_all_hero_values, squeeze_values_together
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
        'startingMoney': 5.0,
        'transferInfo': {
            'transferWildcard': False,
            "transferBlockedDuringPeriod": True,
            # "transferDelayMinutes": 60,
            # "noWildcardForLateRegister": True,
            #'transferLimit': 5
        },
        "extraStats": ["wins", "picks", "bans"],
        "periods": [
            {"start": "2019-05-14 10:00", "end": "2019-05-14 21:00", "multiplier": 1},
            {"start": "2019-05-15 10:00", "end": "2019-05-15 21:00", "multiplier": 1},
            {"start": "2019-05-16 10:00", "end": "2019-05-16 21:00", "multiplier": 1},
            {"start": "2019-05-17 10:00", "end": "2019-05-17 21:00", "multiplier": 1},
        ],
        "url": url,
        "applyPointsAtStartTime": False
    }
    # 60 group games, 31 mainstage
    pickees = []
    calib_tournaments = [10560, 10575, 10733, 10681, 10532, 10646, 10153]
    #hero_values = squeeze_values_together(calibrate_all_hero_values(calib_tournaments, 1549241783))
    for id, name in herodict.items():
        pickees.append({"id": id, "name": name, "value": 1.0})#hero_values[id]})
        #pickees.append({"id": id, "name": name, "value": hero_values[id]})
    data['pickees'] = pickees

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
            API_URL + "leagues/" + str(DEFAULT_LEAGUE), data=json.dumps({'transferOpen': True, 'transferDelayMinutes': None}), headers={
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
    create_league("OGA Dota Pit 2019", 10869, "https://liquipedia.net/dota2/Dota_Pit_League/Season_7")
