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
    picks_bans = [
        {"is_pick": False, "hero_id": 66, "team": 0},
        {"is_pick": False, "hero_id": 80, "team": 0},
        {"is_pick": False, "hero_id": 52, "team": 0},
        {"is_pick": False, "hero_id": 33, "team": 1},
        {"is_pick": False, "hero_id": 120, "team": 1},
        {"is_pick": False, "hero_id": 53, "team": 1},
        {"is_pick": True, "hero_id": 111, "team": 0},
        {"is_pick": True, "hero_id": 15, "team": 0},
        {"is_pick": True, "hero_id": 90, "team": 1},
        {"is_pick": True, "hero_id": 106, "team": 1},
        {"is_pick": False, "hero_id": 55, "team": 0},
        {"is_pick": False, "hero_id": 38, "team": 0},
        {"is_pick": False, "hero_id": 88, "team": 1},
        {"is_pick": False, "hero_id": 54, "team": 1},
        {"is_pick": True, "hero_id": 107, "team": 0},
        {"is_pick": True, "hero_id": 57, "team": 0},
        {"is_pick": True, "hero_id": 100, "team": 1},
        {"is_pick": True, "hero_id": 114, "team": 1},
        {"is_pick": False, "hero_id": 45, "team": 0},
        {"is_pick": False, "hero_id": 10, "team": 1},
        {"is_pick": True, "hero_id": 70, "team": 0},
        {"is_pick": True, "hero_id": 69, "team": 1},
    ]
    add_game_manually(
        'Chaos', 'Team Liquid', True, 1111, picks_bans, 1552830900, 1552833540
    )
