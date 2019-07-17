import json
import urllib2
from collections import namedtuple

import datetime

import os
from fantasydota.lib.constants import API_URL, DEFAULT_LEAGUE, HERO_LEAGUE
from fantasydota.lib.match import iterate_matches, BANS, STAGE_2_MAX, STAGE_1_MAX, result_to_points
from fantasydota.lib.valve_requests import get_league_match_list, get_match_details, \
    dont_piss_off_valve_but_account_for_sporadic_failures

FE_APIKEY = os.environ.get("FE_APIKEY")
if not FE_APIKEY:
    print "Set your fantasy esport APIKEY environment variable"
    exit()

API_LEAGUE_RESULTS_URL = "{}results/leagues/{}".format(API_URL, DEFAULT_LEAGUE)


def check_if_was_allpick_remade(result):
    return sum(p['last_hits'] for p in result['players']) < 10


def check_22_picks(result):
    return len(result.get("picks_bans", [])) == 22


def get_matches(tournament_id, tstamp_from=0, excluded_match_ids=None, highest_series_id=0):
    next_series_id = highest_series_id + 1
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
            add_match_to_api(result)
            add_heroes_results(result, series_id)
            next_series_id += 1
    for pick_ban_tuple in set(saved_ap_remade_matches.keys()).intersection(set(saved_m22_matches.keys())):
        print("match {} was all-pick remade".format(pick_ban_tuple))
        base_result = saved_ap_remade_matches[pick_ban_tuple]
        m22_result = saved_m22_matches[pick_ban_tuple]
        base_result['radiant_win'] = m22_result['radiant_win']

    for k in set(saved_ap_remade_matches.keys()).difference(set(saved_m22_matches.keys())):
        print("ERROR: {} did not have proper stats. but could not find drafted game".format(saved_ap_remade_matches[k]['match_id']))

    for k in set(saved_m22_matches.keys()).difference(set(saved_ap_remade_matches.keys())):
        print("ERROR: {} did not have 22 pick bans but wasnt remade".format(saved_m22_matches[k]['match_id']))


def add_heroes_results(match, series_id):
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
        results.append(Result(hero_id=value["hero_id"], is_team_one=is_team_one, ban=ban, win=win,
                              points=result_to_points(stage, ban, win)))

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
    print('id {}: {} vs {}. radiant win: {}'.format(
        match_id, match.get('radiant_name', ' ').encode('utf-8'), match.get('dire_name', ' ').encode('utf-8'),
        match['radiant_win']
    ))

    data = json.dumps({
        'seriesId': series_id,
        'matches': [{
            'matchId': match_id,
            'teamOneMatchScore': 1 if match['radiant_win'] else 0,
            'teamTwoMatchScore': 0 if match['radiant_win'] else 0,
            'startTstamp': start_time,
            'pickeeResults': pickees
        }]
    })

    try:
        req = urllib2.Request(API_LEAGUE_RESULTS_URL, data=data,
                              headers={'apiKey': FE_APIKEY, "Content-Type": "application/json"})
        response = urllib2.urlopen(req)
        print(response.read())
    except urllib2.HTTPError as e:
        print(e.read())


def add_match_to_api(match):

    odota_info = dont_piss_off_valve_but_account_for_sporadic_failures(
        "https://api.opendota.com/api/matches/{}".format(match['match_id'])
    )
    players = odota_info['players']
    pickees = []
    for player in players:
        pickee = {"id": player["account_id"], "isTeamOne": player["isRadiant"],
                  'stats': [
                      {'field': 'kills', 'value': player["kills"]},
                      {'field': 'deaths', 'value': player["deaths"]},
                      {'field': 'last_hits', 'value': player["last_hits"]},
                      {'field': 'denies', 'value': player["denies"]},
                      {'field': 'first blood', 'value': player["firstblood_claimed"]},
                      {'field': 'stun seconds', 'value': player["stuns"]},
                      {'field': 'teamfight participation', 'value': player["teamfight_participation"]},
                      {'field': 'GPM', 'value': player["gold_per_min"]},
                      {'field': 'tower kills', 'value': player["towers_killed"]},
                      {'field': 'observer wards', 'value': player["obs_placed"]},
                      {'field': 'dewards', 'value': player["observer_kills"]},
                      {'field': 'camps stacked', 'value': player["camps_stacked"]},
                      {'field': 'runes', 'value': player["rune_pickups"]},
                      {'field': 'roshan kills', 'value': player["roshan_kills"]},
                  ]
                  }
        pickees.append(pickee)

    match_id = int(match['match_id'])
    start_time = datetime.datetime.fromtimestamp(match['start_time']).strftime('%Y-%m-%d %H:%M:%S')
    radiant_team = match.get('radiant_name', ' ')
    dire_team = match.get('dire_name', ' ')
    print(match['start_time'])
    print(start_time)
    print('id {}: {} vs {}. radiant win: {}'.format(
        match_id, radiant_team, dire_team, match['radiant_win']
    ))
    latest_series = get_latest_series(radiant_team, dire_team)
    reverse_radiant_t1 = latest_series["teamOne"] == dire_team
    team_one_series_score = latest_series['seriesTeamOneCurrentScore']
    team_two_series_score = latest_series['seriesTeamTwoCurrentScore']
    team_one_win = ((match['radiant_win'] and not reverse_radiant_t1) or (reverse_radiant_t1 and not match['radiant_win']))
    if team_one_win:
        team_one_series_score += 1
    else:
        team_two_series_score += 1
    series_finished = (team_one_series_score + team_two_series_score) >= (latest_series['bestOf'] + 1) / 2
    data = {
        'seriesId': latest_series["seriesId"],
        'seriesTeamOneCurrentScore': team_one_series_score,
        'seriesTeamTwoCurrentScore': team_two_series_score,
        'matches': [{
            'matchId': match_id,
            'teamOneMatchScore': 1 if team_one_win else 0,
            'teamTwoMatchScore': 1 if not team_one_win else 0,
            'startTstamp': start_time,
            'pickeeResults': pickees
        }]
    }
    if series_finished:
        data['seriesTeamOneFinalScore'] = team_one_series_score
        data['seriesTeamTwoFinalScore'] = team_two_series_score
    try:
        req = urllib2.Request(API_LEAGUE_RESULTS_URL, data=json.dumps(data), headers={'apiKey': FE_APIKEY, "Content-Type": "application/json"})
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
    return existing_matches


def get_latest_series(team_one, team_two):
    series_info = json.load(urllib2.urlopen(urllib2.Request(
        "http://localhost/api/v1/results/leagues/" + str(HERO_LEAGUE) + "/findByTeams",
        headers={'apiKey': FE_APIKEY, "Content-Type": "application/json"},
        data=json.dumps({'teamOne': team_one, 'teamTwo': team_two, 'includeReversedTeams': True})
    )))[-1]
    return series_info


def main():
    # it sounds sensibile to save work by checking highest startTstamp, and filtering out any below
    # this is not safe because can 'lose' games that started before highest startTstamp, but went on so long
    # that highest startTstamp finished first
    existing_matches = get_already_stored_matches()
    excluded_matches = [m["match"]["matchId"] for s in existing_matches for m in s["matches"]]
    highest_series_id = next((s["seriesId"] for s in excluded_matches), 0)
    print("excluded matches: {}".format(excluded_matches))
    # 1551814635
    get_matches(10869, excluded_match_ids=excluded_matches, tstamp_from=1556223758, highest_series_id=highest_series_id)


if __name__ == "__main__":
    main()
