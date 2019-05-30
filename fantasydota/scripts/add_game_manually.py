import datetime

import json
import os
import sys

import re
import urllib2

from fantasydota.lib.constants import DEFAULT_LEAGUE
from fantasydota.lib.herodict import herodict
from fantasydota.scripts.get_dota_results import API_LEAGUE_RESULTS_URL


def add_game_manually(
        match_id, tournament_id, team_one=None, team_two=None, team_one_score=None, team_two_score=None, target_at_tstamp=None
):
    all_pickees = json.loads(urllib2.urlopen(urllib2.Request("http://localhost/api/v1/pickees/" + str(DEFAULT_LEAGUE))).read())
    FE_APIKEY = os.environ.get("FE_APIKEY")
    if not FE_APIKEY:
        print "Set your fantasy esport APIKEY environment variable"
        exit()
    pickees = [{'id': all_pickees[0]['id'], 'isTeamOne': True, 'stats': [
        {'field': 'goal', 'value': 2}, {'field': 'WhoScored match rating', 'value': 8.6},{'field': 'clean sheet', 'value': 1}
    ]}]
    data = json.dumps({
        'matchId': match_id,
        'teamOneScore': team_one_score,
        'teamTwoScore': team_two_score,
        'tournamentId': tournament_id,
        'pickees': pickees
    })
    if target_at_tstamp is not None:
        data['targetAtTstamp'] = datetime.datetime.fromtimestamp(target_at_tstamp).strftime('%Y-%m-%d %H:%M:%S')
    if team_one is not None:
        data['teamOne'] = team_one
        data['teamTwo'] = team_two
    try:
        req = urllib2.Request(API_LEAGUE_RESULTS_URL, data=data,
                              headers={'apiKey': FE_APIKEY, "Content-Type": "application/json"})
        response = urllib2.urlopen(req)
        print(response.read())
    except urllib2.HTTPError as e:
        print(e.read())


if __name__ == "__main__":
    regex = re.compile('[^a-zA-Z]')
    heroes_simple_rev = {regex.sub('', v.lower()).replace(' ', ''): k for k, v in herodict.items()}
    picks_bans = []
    #team_one, team_two, radiant_win, fake_id, start_time, target_time = sys.argv[1:7]
    add_game_manually(
        0, 1, team_one_score=6, team_two_score=4
    )
