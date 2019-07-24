import urllib2

import json

import os

from fantasydota.lib.calibration import calibrate_all_hero_values, squeeze_values_together
from fantasydota.lib.herodict import herodict
from fantasydota.lib.constants import API_URL, DEFAULT_LEAGUE

FE_APIKEY = os.environ.get("FE_APIKEY")
if not FE_APIKEY:
    print "Set your fantasy esport APIKEY environment variable"


def create_league(name, tournament_id, url):

    periods = []
    for day in ([15, 16, 17, 18, 20, 21, 22, 23, 24, 25]):
        if day < 20:
            multiplier = 1.0
        elif day < 25:
            multiplier = 2.0
        else:
            multiplier = 3.0
        periods.append({'start': '2019-08-{} 00:00'.format(day), 'end': '2019-08-{} 00:00'.format(day+1), 'multiplier': multiplier})

    pickees = []
    calib_tournaments = [10989, 10826, 10979, 10944, 10616, 10749, 11109, 11115, 11099]
    hero_values = squeeze_values_together(calibrate_all_hero_values(calib_tournaments, 1561148316))
    for id, name in herodict.items():
        pickees.append({"id": id, "name": name, "value": hero_values[id]})
    with open(os.getcwd() + "/../miscdata/pickee_calibration.json", "w+") as f:
        json.dump(pickees, f)
    # with open(os.getcwd() + "/../miscdata/pickee_calibration.json") as f:
    #     pickees = json.load(f)

    data = {
        'name': name,
        'apiKey': FE_APIKEY,
        'tournamentId': tournament_id,
        'gameId': 1,
        'pickeeDescription': 'Hero',
        'periodDescription': 'Day',
        'startingMoney': 50.0,
        'teamSize': 5,
        'transferInfo': {
            'isCardSystem': False,
            'transferWildcard': True,
            "transferBlockedDuringPeriod": True,
            'transferLimit': 10,
            'noWildcardForLateRegister': True,
        },
        "periods": periods,
        "url": url,
        "applyPointsAtStartTime": True,
        "manuallyCalculatePoints": True,
        "stats": [
            {'name': 'picks'},
            {'name': 'bans'},
            {'name': 'wins'},
        ],
        'pickees': pickees
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


if __name__ == "__main__":
    create_league("The International 2019 Heroes", 10749, "https://liquipedia.net/dota2/The_International/2019")
