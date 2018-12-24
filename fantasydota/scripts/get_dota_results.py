import json
import os
import re
import time
import urllib2
import traceback
from collections import namedtuple

APIKEY = os.environ.get("APIKEY")
if not APIKEY:
    print "Set your APIKEY environment variable"
LEAGUE_LISTING = "http://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v0001?key=%s" % APIKEY

INTERNAL_API_URL = "http://localhost:9000/api/v1/results"

BANS = list(range(6) + range(10, 14) + range(18, 20))
STAGE_1_MAX = 9
STAGE_2_MAX = 17

Result = namedtuple('Result', 'points ban win')


def dont_piss_off_valve_but_account_for_sporadic_failures(req_url):
    print("requesting {0}".format(req_url))
    fuck = True  # no idea why this failing. im waiting long enough to not piss off valve?
    sleep_time = 1
    fucks_given = 5
    while fuck and fucks_given:
        try:
            req = urllib2.Request(req_url, headers={'User-Agent': 'ubuntu:fantasydotaheroes:v1.0.0 (by /u/LePianoDentist)'})
            response = urllib2.urlopen(req)
            fuck = False
        except:
            sleep_time += 30  # incase script breaks dont want to spam
            print "Why the fuck are you fucking failing you fucker"
            traceback.print_exc()
            fucks_given -= 1
            time.sleep(sleep_time)
            continue
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


def result_to_points(stage, ban, win):
    if stage == 1:
        if ban:
            return 1
        elif win:
            return 9
        else:
            return -5
    elif stage == 2:
        if ban:
            return 2
        elif win:
            return 11
        else:
            return -4
    else:
        if ban:
            return 4
        elif win:
            return 15
        else:
            return -5


def add_match_to_api(tournament_id, match):
    match_id = int(match['match_id'])
    picks = match.get("picks_bans", [])
    if len(picks) < 22:
        print("MatchID: %s fucked up picks bans. not 22" % match_id)
        # Sometimes they attach 1v1 games, or failed lobbies to the tournament ticket
        return

    team_one_victory = match['radiant_win']
    results = []

    for key, value in enumerate(picks):
        key = int(key)
        is_team_one = (value["team"] == 0)
        win = (is_team_one == team_one_victory)
        ban = key in BANS
        if key > STAGE_2_MAX:
            stage = 3
        elif key > STAGE_1_MAX:
            stage = 2
        else:
            stage = 1
        results.append(Result(ban=ban, win=win, points=result_to_points(stage, ban, win)))

    data = json.dumps({
        'matchId': match_id,
        'teamOne': match.get('radiant_name'),
        'teamTwo': match.get('dire_name'),
        'teamOneVictory': match['radiant_win'],
        'tournamentId': tournament_id,
        'startTimestamp': match['start_time']
    })
    req = urllib2.Request(
        INTERNAL_API_URL, data=data, headers={'User-Agent': 'ubuntu:fantasydotaheroes:v1.0.0 (by /u/LePianoDentist)'}
    )
    response = urllib2.urlopen(req)
    print(response)


def add_matches(tournament_id, tstamp_from=0):
    match_list_json = get_league_match_list(tournament_id)

    matches = [(match["match_id"], match["series_id"]) for match in match_list_json["result"]["matches"]
               if match["start_time"] > tstamp_from]
    print "matches", matches
    for match, series_id in matches:
        add_match_to_api(tournament_id, get_match_details(match)["result"])


def main():
    add_matches(9870, tstamp_from=1534332914)

if __name__ == "__main__":
    main()
