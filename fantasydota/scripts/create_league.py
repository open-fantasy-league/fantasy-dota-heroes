import urllib2

from fantasydota.lib import herodict
from fantasydota.scripts.get_dota_results import INTERNAL_API_URL


def create_league(name, tournament_id, url):

    data = {
        'name': name,
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
    for id, name in herodict.items():
        pickees.append({"id": id, "name": name, "value": 20.0})
    data['pickees'] = pickees

    req = urllib2.Request(
        INTERNAL_API_URL, data=data, headers={'User-Agent': 'ubuntu:fantasydotaheroes:v1.0.0 (by /u/LePianoDentist)'}
    )
    response = urllib2.urlopen(req)


if __name__ == "__main__":
    create_league("TI8", 9870, "www.yeah")
