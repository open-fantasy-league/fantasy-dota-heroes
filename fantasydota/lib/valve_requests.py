import traceback
import urllib2

import time

import json

import os

APIKEY = os.environ.get("APIKEY")
if not APIKEY:
    print "Set your VALVE APIKEY environment variable"

LEAGUE_LISTING = "http://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v0001?key=%s" % APIKEY


def dont_piss_off_valve_but_account_for_sporadic_failures(req_url):
    print("requesting {0}".format(req_url))
    fuck = True  # no idea why this failing. im waiting long enough to not piss off valve?
    sleep_time = 1
    fucks_given = 10
    while fuck and fucks_given:
        try:
            req = urllib2.Request(req_url, headers={'User-Agent': 'ubuntu:fantasydotaheroes:v1.0.0 (by /u/LePianoDentist)'})
            response = urllib2.urlopen(req)
            fuck = False
        except:
            time.sleep(sleep_time)
            sleep_time *= 3  # incase script breaks dont want to spam
            print "Why the fuck are you fucking failing you fucker"
            traceback.print_exc()
            fucks_given -= 1
            continue
    time.sleep(sleep_time)
    data = json.load(response)
    return data


def get_league_match_list(league_id):
    return dont_piss_off_valve_but_account_for_sporadic_failures(
        "http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v0001?" \
        "key=%s&league_id=%s" % (APIKEY, league_id))


def get_match_details(match_id):
    return dont_piss_off_valve_but_account_for_sporadic_failures(
        "http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v0001?" \
        "key=%s&match_id=%s" % (APIKEY, match_id))
