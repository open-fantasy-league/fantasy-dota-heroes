import json
import urllib2
from collections import namedtuple

import time

import datetime
from fantasydota.lib.constants import API_URL, DEFAULT_LEAGUE
from fantasydota.lib.match import iterate_matches, BANS, STAGE_2_MAX, STAGE_1_MAX, result_to_points

API_RESULTS_URL = API_URL + "results"
Result = namedtuple('Result', 'hero_id is_team_one points ban win')


def add_match_to_api(match, tournament_id=None):
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
    url = API_RESULTS_URL + "/" + str(DEFAULT_LEAGUE)
    print(url)
    try:
        req = urllib2.Request(
            url, data=data, headers={
                'User-Agent': 'ubuntu:fantasydotaheroes:v1.0.0 (by /u/LePianoDentist)',
                "Content-Type": "application/json"
            }
        )
        response = urllib2.urlopen(req)
        print(response.read())
    except urllib2.HTTPError as e:
        print(e.read())


def main():
    iterate_matches(9870, add_match_to_api, tstamp_from=1534332914)

if __name__ == "__main__":
    main()
