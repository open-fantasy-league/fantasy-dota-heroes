import json
import urllib2
from collections import namedtuple

import datetime

import os
from fantasydota.lib.constants import API_URL, DEFAULT_LEAGUE
from fantasydota.lib.match import iterate_matches, BANS, STAGE_2_MAX, STAGE_1_MAX, result_to_points

API_LEAGUE_RESULTS_URL = "{}results/leagues/{}".format(API_URL, DEFAULT_LEAGUE)

def add_match_to_api(match, tournament_id=None):
    FE_APIKEY = os.environ.get("FE_APIKEY")
    if not FE_APIKEY:
        print "Set your fantasy esport APIKEY environment variable"

    Result = namedtuple('Result', 'hero_id is_team_one points ban win')

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
        results.append(Result(hero_id=value["hero_id"], is_team_one=is_team_one, ban=ban, win=win, points=result_to_points(stage, ban, win)))

    pickees = []
    for r in results:
        entry = {'id': r.hero_id, 'isTeamOne': r.is_team_one, 'stats': [{'field': 'points', 'value': r.points}]}
        if r.ban:
            entry['stats'].append({'field': 'bans', 'value': 1})
        else:
            entry['stats'].append({'field': 'picks', 'value': 1})
            if r.win:
                entry['stats'].append({'field': 'wins', 'value': 1})
        pickees.append(entry)
    print(match['start_time'])
    print(datetime.datetime.fromtimestamp(match['start_time']).strftime('%Y-%m-%d %H:%M:%S'))
    data = json.dumps({
        'matchId': match_id,
        'teamOne': match.get('radiant_name', ' '),
        'teamTwo': match.get('dire_name', ' '),
        'teamOneVictory': match['radiant_win'],
        'tournamentId': tournament_id,
        'startTstamp': datetime.datetime.fromtimestamp(match['start_time']).strftime('%Y-%m-%d %H:%M:%S'),
        'pickees': pickees
    })
    try:
        req = urllib2.Request(API_LEAGUE_RESULTS_URL, data=data, headers={'apiKey': FE_APIKEY, "Content-Type": "application/json"})
        response = urllib2.urlopen(req)
        print(response.read())
    except urllib2.HTTPError as e:
        print(e.read())


def get_already_stored_matches():
    try:
        req = urllib2.Request(API_LEAGUE_RESULTS_URL,
                              headers={"Content-Type": "application/json"})
        response = urllib2.urlopen(req)
        existing_matches = json.loads(response.read())
    except urllib2.HTTPError as e:
        print(e.read())
        raise e

    existing_ids = [m["match"]["id"] for m in existing_matches]
    return existing_ids


def main():
    # it sounds sensibile to save work by checking highest startTstamp, and filtering out any below
    # this is not safe because can 'lose' games that started before highest startTstamp, but went on so long
    # that highest startTstamp finished first
    excluded_matches = get_already_stored_matches()
    print(excluded_matches)
    iterate_matches(10424, add_match_to_api, excluded_match_ids=excluded_matches, tstamp_from=1534332914)

if __name__ == "__main__":
    main()
