from fantasydota.lib.constants import API_URL
from fantasydota.lib.valve_requests import get_league_match_list, get_match_details

API_RESULTS_URL = API_URL + "results"

BANS = list(range(6) + range(10, 14) + range(18, 20))
STAGE_1_MAX = 9
STAGE_2_MAX = 17


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


def update_hero_calibration_dict(match, hero_calibration_dict=None, **kwargs):
    match_id = int(match['match_id'])
    picks = match.get("picks_bans", [])
    if len(picks) < 22:
        print("MatchID: %s fucked up picks bans. not 22" % match_id)
        # Sometimes they attach 1v1 games, or failed lobbies to the tournament ticket
        return

    team_one_victory = match['radiant_win']

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
        hero_calibration_dict[value["hero_id"]] += result_to_points(stage, ban, win)


def iterate_matches(tournament_id, func, tstamp_from=0, **kwargs):
    match_list_json = get_league_match_list(tournament_id)

    matches = [(match["match_id"], match["series_id"]) for match in match_list_json["result"]["matches"]
               if match["start_time"] > tstamp_from]
    print "matches", matches
    for match, series_id in matches:
        kwargs['tournament_id'] = tournament_id
        func(get_match_details(match)["result"], **kwargs)
