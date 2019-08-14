import os

import json
import urllib2

from fantasydota.lib.constants import TI9, API_URL, DEFAULT_LEAGUE

FE_APIKEY = os.environ.get("FE_APIKEY")
if not FE_APIKEY:
    print "Set your fantasy esport APIKEY environment variable"


def get_fixtures():
    with open(os.getcwd() + "/../miscdata/fixtures.json") as f:
        fixtures = json.load(f)
    series = []
    for i, match in enumerate(fixtures):
        series.append({
            'seriesId': i, 'tournamentId': TI9, 'teamOne': match[0], 'teamTwo': match[1], "startTstamp": match[2],
            "matches": [], "bestOf": match[3]
        })
    return series


def main():
    for fixture in get_fixtures():
        try:
            req = urllib2.Request(
                API_URL + "results/leagues/" + str(DEFAULT_LEAGUE),
                data=json.dumps(fixture), headers={
                    "Content-Type": "application/json",
                    "apiKey": FE_APIKEY
                }
            )
            response = urllib2.urlopen(req)
            print(response.read())
        except urllib2.HTTPError as e:
            print(e.read())


if __name__ == '__main__':
    main()
