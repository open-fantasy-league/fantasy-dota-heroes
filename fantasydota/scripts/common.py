import os

import json
import urllib2

from fantasydota.lib.constants import DEFAULT_LEAGUE, API_URL

FE_APIKEY = os.environ.get("FE_APIKEY")
if not FE_APIKEY:
    print "Set your fantasy esport APIKEY environment variable"
    exit()


def simplify_team_names(name):
    return name.replace('AFC B', 'B').replace('& Hove Albion', '').replace("Man City", "Manchester City").\
        replace("Man Utd", "Manchester United").replace('Sheff Utd', 'Sheffield United')


def all_pickees():
    return json.load(urllib2.urlopen(urllib2.Request(API_URL + "pickees/" + str(DEFAULT_LEAGUE))))


def update_pickees(diffs, inserts):
    try:
        req = urllib2.Request(
            API_URL + "pickees/leagues/" + str(DEFAULT_LEAGUE) + "/updates",
            data=json.dumps(diffs), headers={
                "Content-Type": "application/json",
                "apiKey": FE_APIKEY
            }
        )
        response = urllib2.urlopen(req).read()
        print(response)
    except urllib2.HTTPError as e:
        print(e.read())
        raise

    try:
        req = urllib2.Request(
            API_URL + "pickees/leagues/" + str(DEFAULT_LEAGUE) + "/add",
            data=json.dumps(inserts), headers={
                "Content-Type": "application/json",
                "apiKey": FE_APIKEY
            }
        )
        response = urllib2.urlopen(req).read()
        print(response)
    except urllib2.HTTPError as e:
        print(e.read())
        raise
