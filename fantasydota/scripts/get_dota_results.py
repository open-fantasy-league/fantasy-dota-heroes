import json
import urllib2
from collections import namedtuple

import datetime

import os
from fantasydota.lib.constants import API_URL, DEFAULT_LEAGUE, HERO_LEAGUE, TEAM_IDS_TO_NAMES, TI9
from fantasydota.lib.match import iterate_matches, BANS, STAGE_2_MAX, STAGE_1_MAX, result_to_points
from fantasydota.lib.valve_requests import get_league_match_list, get_match_details, \
    dont_piss_off_valve_but_account_for_sporadic_failures

valid_pickee_ids = [119631156, 6922000,10366616,19672354,21289303,25907144,26771994,34505203,41231571,54580962,72312627,73562326,77490514,82262664,84772440,86698277,86700461,86726887,86727555,86738694,86745912,86799300,87012746,87278757,87382579,88271237,89117038,89423756,91443418,92423451,94054712,94155156,94296097,94738847,97590558,98172857,100471531,101356886,101695162,102099826,103735745,105248644,106573901,106863163,107803494,108452107,111030315,111620041,113457795,114619230,116585378,117421467,119576842,121769650,125581247,132851371,134276083,134556694,135878232,137193239,139822354,139876032,139937922,142139318,143693439,145550466,148215639,152545459,152962063,153836240,154715080,155494381,157989498,159020918,164532005,164685175,169025618,171981096,173476224,182331313,184950344,186627166,192914280,221666230,234699894,255219872,292921272,311360822,397462905,401792574,412753955]

FE_APIKEY = os.environ.get("FE_APIKEY")
if not FE_APIKEY:
    print "Set your fantasy esport APIKEY environment variable"
    exit()

API_LEAGUE_RESULTS_URL = "{}results/leagues/".format(API_URL)

#MATCH_OVERRIDES = {4968140678: 4968169805}
EXTRA_EXCLUDE = [4968140678]
def check_if_was_allpick_remade(result):
    return sum(p['last_hits'] for p in result['players']) < 10


def check_22_picks(result):
    return len(result.get("picks_bans", [])) == 22

def get_matches(tournament_id, tstamp_from=0, excluded_match_ids=None, highest_series_id=0):
    #TODO remove tstamp_from = 0
    next_series_id = highest_series_id + 1
    excluded_match_ids = EXTRA_EXCLUDE + (excluded_match_ids or [])
    print("excluded matches: {}".format(excluded_match_ids))
    match_list_json = get_league_match_list(tournament_id)

    matches = [(match["match_id"], match["series_id"]) for match in match_list_json["result"]["matches"]
               if match["start_time"] >= tstamp_from and match["match_id"] not in excluded_match_ids]
    #matches = [(4978383071, 99999998), (4978435281, 99999997), (4978505997, 99999996), (4978587076, 99999995), (4978701632, 99999994)]
    #matches = [(4080856812, 123)]
    print "matches", matches
    saved_ap_remade_matches = {}
    saved_m22_matches = {}

    for match, series_id in reversed(matches):
        result = get_match_details(match)["result"]
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
            print("normal match:")
            radiant_team_id = result.get('radiant_team_id', 0)
            dire_team_id = result.get('dire_team_id', 0)
            #radiant_team_id, dire_team_id = (6209804, 15)
            radiant_team = TEAM_IDS_TO_NAMES[radiant_team_id]
            dire_team = TEAM_IDS_TO_NAMES[dire_team_id]
            print("{} vs {}".format(radiant_team, dire_team))
            add_match_to_api(result, radiant_team, dire_team)
            add_heroes_results(result, radiant_team, dire_team, match)
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


def add_heroes_results(match, radiant_team, dire_team, series_id):
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
        'teamOne': radiant_team,
        'teamTwo': dire_team,
        'matches': [{
            'matchId': match_id,
            'teamOneMatchScore': 1 if match['radiant_win'] else 0,
            'teamTwoMatchScore': 0 if match['radiant_win'] else 0,
            'startTstamp': start_time,
            'pickeeResults': pickees
        }]
    })

    try:
        req = urllib2.Request(API_LEAGUE_RESULTS_URL + str(HERO_LEAGUE), data=data,
                              headers={'apiKey': FE_APIKEY, "Content-Type": "application/json"})
        response = urllib2.urlopen(req)
        print(response.read())
    except urllib2.HTTPError as e:
        print(e.read())


def add_match_to_api(match, radiant_team, dire_team):

    odota_info = dont_piss_off_valve_but_account_for_sporadic_failures(
        "https://api.opendota.com/api/matches/{}".format(match['match_id'])
    )
    players = odota_info['players']
    pickees = []
    for player in players:
        pickee = {"id": player["account_id"], "isTeamOne": player["isRadiant"],
                  'stats': [
                      {'field': 'kills', 'value': player["kills"]},
                      {'field': 'assists', 'value': player["assists"]},
                      {'field': 'deaths', 'value': player["deaths"]},
                      {'field': 'last hits', 'value': player["last_hits"]},
                      {'field': 'denies', 'value': player["denies"]},
                      {'field': 'first blood', 'value': player["firstblood_claimed"]},
                      #{'field': 'stun', 'value': player["stuns"]},
                      {'field': 'teamfight participation', 'value': player["teamfight_participation"]},
                      {'field': 'GPM', 'value': player["gold_per_min"]},
                      {'field': 'towers', 'value': player["towers_killed"]},
                      {'field': 'observer wards', 'value': player["obs_placed"]},
                      {'field': 'dewards', 'value': player["observer_kills"]},
                      {'field': 'camps stacked', 'value': player["camps_stacked"]},
                      {'field': 'runes', 'value': player["rune_pickups"]},
                      {'field': 'roshans', 'value': player["roshan_kills"]},
                  ]
                  }
        if player["account_id"] in valid_pickee_ids:
            pickees.append(pickee)

    match_id = int(match['match_id'])
    start_time = datetime.datetime.fromtimestamp(match['start_time']).strftime('%Y-%m-%d %H:%M:%S')
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
    series_finished = (team_one_series_score + team_two_series_score) > (latest_series['bestOf'] + 1) / 2.0
    data = {
        'seriesId': latest_series["seriesId"],
        'seriesTeamOneCurrentScore': team_one_series_score,
        'seriesTeamTwoCurrentScore': team_two_series_score,
        'matches': [{
            'matchId': match_id,
            #'matchId': match_id + 1,
            'teamOneMatchScore': 1 if team_one_win else 0,
            'teamTwoMatchScore': 1 if not team_one_win else 0,
            'startTstamp': start_time,
            'pickeeResults': pickees
        }]
    }
    if series_finished:
        data['seriesTeamOneFinalScore'] = team_one_series_score
        data['seriesTeamTwoFinalScore'] = team_two_series_score
    print(data)
    try:
        req = urllib2.Request(API_LEAGUE_RESULTS_URL + str(DEFAULT_LEAGUE), data=json.dumps(data), headers={'apiKey': FE_APIKEY, "Content-Type": "application/json"})
        response = urllib2.urlopen(req)
        print(response.read())
    except urllib2.HTTPError as e:
        print(e.read())


def get_already_stored_matches():
    try:

        req = urllib2.Request(API_LEAGUE_RESULTS_URL + str(DEFAULT_LEAGUE),
                              headers={"Content-Type": "application/json"})
        response = urllib2.urlopen(req)
        existing_matches = json.loads(response.read())
    except urllib2.HTTPError as e:
        print(e.read())
        raise e
    return existing_matches


def get_latest_series(team_one, team_two):
    series_info = json.load(urllib2.urlopen(urllib2.Request(
        API_URL + "results/leagues/" + str(DEFAULT_LEAGUE) + "/findByTeams",
        headers={'apiKey': FE_APIKEY, "Content-Type": "application/json"},
        data=json.dumps({'teamOne': team_one, 'teamTwo': team_two, 'includeReversedTeams': True})
    )))
    print(series_info)
    print(list(sorted(series_info, key=lambda x: x['series']['seriesId']))[-1])
    print("\n"*20)
    print(list(sorted(series_info, key=lambda x: x['series']['seriesId']))[0])
    return list(sorted(series_info, key=lambda x: x['series']['seriesId']))[-1]["series"]


def main():
    # it sounds sensibile to save work by checking highest startTstamp, and filtering out any below
    # this is not safe because can 'lose' games that started before highest startTstamp, but went on so long
    # that highest startTstamp finished first
    existing_matches = get_already_stored_matches()
    excluded_matches = [m["match"]["matchId"] for s in existing_matches for m in s["matches"]] + [4982304736] # +allstar match
    highest_series_id = next((s["series"]["seriesId"] for s in existing_matches), 0)
    print("excluded matches: {}".format(excluded_matches))
    # 1551814635
    get_matches(TI9, excluded_match_ids=excluded_matches, tstamp_from=1565750963, highest_series_id=highest_series_id)


if __name__ == "__main__":
    main()
