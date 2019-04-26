import sys

import re

from fantasydota.lib.herodict import herodict
from fantasydota.scripts.get_dota_results import add_match_to_api


def add_game_manually(radiant_team, dire_team, radiant_win, fake_match_id, pick_bans, start_time, target_at_tstamp):
    match_dict = {"radiant_name": radiant_team,
                  "dire_name": dire_team,
                  "match_id": fake_match_id,
                  "radiant_win": radiant_win,
                  "pick_bans": pick_bans,
                  "start_time": start_time
                  }
    add_match_to_api(match_dict, tournament_id=10681, target_at_tstamp=target_at_tstamp)


if __name__ == "__main__":
    regex = re.compile('[^a-zA-Z]')
    heroes_simple_rev = {regex.sub('', v.lower()).replace(' ', ''): k for k, v in herodict.items()}
    picks_bans = []
    team_one, team_two, radiant_win, fake_id, start_time, target_time = sys.argv[1:7]
    for i, arg in enumerate(sys.argv[7:]):
        hero_id = heroes_simple_rev[arg]
        if i < 3:
            picks_bans.append({"is_pick": False, "hero_id": hero_id, "team": 0})
        elif i < 6:
            picks_bans.append({"is_pick": False, "hero_id": hero_id, "team": 1})
        elif i < 8:
            picks_bans.append({"is_pick": True, "hero_id": hero_id, "team": 0})
        elif i < 10:
            picks_bans.append({"is_pick": True, "hero_id": hero_id, "team": 1})
        elif i < 12:
            picks_bans.append({"is_pick": False, "hero_id": hero_id, "team": 0})
        elif i < 14:
            picks_bans.append({"is_pick": False, "hero_id": hero_id, "team": 1})
        elif i < 16:
            picks_bans.append({"is_pick": True, "hero_id": hero_id, "team": 0})
        elif i < 18:
            picks_bans.append({"is_pick": True, "hero_id": hero_id, "team": 1})
        elif i < 19:
            picks_bans.append({"is_pick": False, "hero_id": hero_id, "team": 0})
        elif i < 20:
            picks_bans.append({"is_pick": False, "hero_id": hero_id, "team": 1})
        elif i < 21:
            picks_bans.append({"is_pick": True, "hero_id": hero_id, "team": 0})
        elif i < 22:
            picks_bans.append({"is_pick": True, "hero_id": hero_id, "team": 1})
    add_game_manually(
        team_one, team_two, radiant_win, fake_id, picks_bans, start_time, target_time
    )
