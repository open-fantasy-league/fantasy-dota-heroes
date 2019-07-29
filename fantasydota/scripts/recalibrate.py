import argparse
import os
import urllib2

import json
from fantasydota.lib.calibration import combine_calibrations, calibrate_value, calibrate_all_hero_values, \
    squeeze_values_together
from fantasydota.lib.constants import API_URL, DEFAULT_LEAGUE, HERO_LEAGUE, TI9

OFFSET = 0.2

def recalibrate():
    FE_APIKEY = os.environ.get("FE_APIKEY")
    if not FE_APIKEY:
        print "Set your fantasy esport APIKEY environment variable"
        exit()

    url = "{}pickees/{}".format(API_URL, DEFAULT_LEAGUE)
    update_url = "{}pickees/leagues/{}/updatePrices".format(API_URL, HERO_LEAGUE)
    req = urllib2.Request(
        url,
    )
    response = urllib2.urlopen(req)
    heroes = json.loads(response.read())
    print(response)
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', nargs='?', help='already calculated filename')
    args = parser.parse_args()
    if args.f:
        with open(os.getcwd() + "/../miscdata/{}".format(args.f), "w+") as f:
            data = {"pickees": [{'id': h['id'], 'price': h['price'] + OFFSET} for h in json.load(f)]}
    else:
        data = {"pickees": []}
        new_calibration = squeeze_values_together(calibrate_all_hero_values([TI9], 1551814635))
        for hero in heroes:
            id_ = hero['id']
            new_value = round(combine_calibrations(hero['value'], new_calibration[id_]), 1)
            print "new calbration %s: %s, from %s" % (id_, new_value, hero['value'])
            data["pickees"].append({'id': id_, 'price': new_value})
    try:
        req = urllib2.Request(
            update_url, data=json.dumps(data), headers={
                "Content-Type": "application/json",
                "apiKey": FE_APIKEY
            }
        )
        response = urllib2.urlopen(req)
        print(response.read())
    except urllib2.HTTPError as e:
        print(e.read())


if __name__ == "__main__":
    recalibrate()

