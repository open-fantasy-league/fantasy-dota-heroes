import json
import urllib2
from collections import namedtuple

import datetime

import os
from fantasydota.lib.constants import API_URL, DEFAULT_LEAGUE
from fantasydota.lib.match import iterate_matches, BANS, STAGE_2_MAX, STAGE_1_MAX, result_to_points
from fantasydota.lib.valve_requests import get_league_match_list, get_match_details

API_LEAGUE_RESULTS_URL = "{}results/leagues/{}".format(API_URL, DEFAULT_LEAGUE)


def check_if_was_allpick_remade(result):
    return sum(p['last_hits'] for p in result['players']) < 10


def check_22_picks(result):
    return len(result.get("picks_bans", [])) == 22


def get_matches(tournament_id, tstamp_from=0, excluded_match_ids=None):
    excluded_match_ids = excluded_match_ids or []
    match_list_json = get_league_match_list(tournament_id)

    matches = [(match["match_id"], match["series_id"]) for match in match_list_json["result"]["matches"]
               if match["start_time"] >= tstamp_from and match["match_id"] not in excluded_match_ids]
    print "matches", matches
    saved_ap_remade_matches = {}
    saved_m22_matches = {}

    for match, series_id in matches:
        result = get_match_details(match)["result"]
        match_id = result['match_id']
        if check_if_was_allpick_remade(result):
            saved_ap_remade_matches[
                frozenset([p['hero_id'] for p in result['players']] +
                          [result.get('radiant_name', 'rad'), result.get('dire_name', 'dire')])
            ] = result
        elif not check_22_picks(result):
            saved_m22_matches[
                frozenset([p['hero_id'] for p in result['players']] +
                          [result.get('radiant_name', 'rad'), result.get('dire_name', 'dire')])
            ] = result
        else:
            # saved_matches[
            #     frozenset([p['hero_id'] for p in result['players']] +
            #               [result.get('radiant_name', 'rad'), result.get('dire_name', 'dire')])
            # ] = result
            add_match_to_api(result, tournament_id=tournament_id)
    for pick_ban_tuple in set(saved_ap_remade_matches.keys()).intersection(set(saved_m22_matches.keys())):
        print("match {} was all-pick remade".format(pick_ban_tuple))
        base_result = saved_ap_remade_matches[pick_ban_tuple]
        m22_result = saved_m22_matches[pick_ban_tuple]
        base_result['radiant_win'] = m22_result['radiant_win']

    for k in set(saved_ap_remade_matches.keys()).difference(set(saved_m22_matches.keys())):
        print("ERROR: {} did not have proper stats. but could not find drafted game".format(saved_ap_remade_matches[k]['match_id']))

    for k in set(saved_m22_matches.keys()).difference(set(saved_ap_remade_matches.keys())):
        print("ERROR: {} did not have 22 pick bans but wasnt remade".format(saved_m22_matches[k]['match_id']))


def add_match_to_api(match, tournament_id=None):
    FE_APIKEY = os.environ.get("FE_APIKEY")
    if not FE_APIKEY:
        print "Set your fantasy esport APIKEY environment variable"
        exit()

    Result = namedtuple('Result', 'hero_id is_team_one points ban win')

    match_id = int(match['match_id'])
    picks = match.get("picks_bans", [])

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
    start_time = datetime.datetime.fromtimestamp(match['start_time']).strftime('%Y-%m-%d %H:%M:%S')
    print(match['start_time'])
    print(start_time)
    print('id {}: {} vs {}. radiant win: {}'.format(match_id, match.get('radiant_name', ' '), match.get('dire_name', ' '), match['radiant_win']))
    data = json.dumps({
        'matchId': match_id,
        'teamOne': match.get('radiant_name', ' '),
        'teamTwo': match.get('dire_name', ' '),
        'teamOneVictory': match['radiant_win'],
        'tournamentId': tournament_id,
        'startTstamp': start_time,
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
    print("excluded matches: {}".format(excluded_matches))
    get_matches(10681, excluded_match_ids=excluded_matches, tstamp_from=1551814635)


if __name__ == "__main__":
    main()
