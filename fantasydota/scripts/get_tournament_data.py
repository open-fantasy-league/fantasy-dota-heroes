import json
import os
import urllib2
import re

import time
import transaction

from fantasydota.lib.session_utils import make_session
from fantasydota.models import Result, HeroGame, ItemBuild, Match, League

APIKEY = os.environ.get("APIKEY")
if not APIKEY:
    print "Set your APIKEY environment variable"
LEAGUE_LISTING = "http://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v0001?key=%s" % APIKEY


def dont_piss_off_valve_but_account_for_sporadic_failures(req_url):
    print("requesting {0}".format(req_url))
    fuck = True  # no idea why this failing. im waiting long enough to not piss off valve?
    sleep_time = 1
    while fuck:
        try:
            response = urllib2.urlopen(req_url)
            time.sleep(sleep_time)
            fuck = False
        except:
            sleep_time += 30  # incase script breaks dont want to spam
            print "Why the fuck are you fucking failing you fucker"
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


def add_matches(session, tournament_id, tstamp_from=0, add_match=True):
    match_list_json = get_league_match_list(tournament_id)

    matches = [(match["match_id"], match["series_id"]) for match in match_list_json["result"]["matches"]
               if match["start_time"] > tstamp_from and match["match_id"] != 3368387319]
    print "matches", matches
    for match, series_id in matches:
        with transaction.manager:
            if session.query(Result).filter(Result.match_id == match).first():  # if old result dont process
                continue

            match_json = get_match_details(match)["result"]
            radiant_win = match_json["radiant_win"]
            try:
                picks = match_json["picks_bans"]
            except KeyError:  # game crashed and they remade with all pick. need to manually
                print "MatchID: %s no picks and bans. Need manually inserting" % match
                continue
            if len(picks) < 22:
                print "MatchID: %s fucked up picks bans. not 22. Check if need update" % match
                continue
            if add_match:
                day = session.query(League.current_day).filter(League.id == tournament_id).first()[0]
                try:
                    session.add(Match(
                        int(match_json["match_id"]), re.sub(r'\W+', '', match_json["radiant_name"]), re.sub(r'\W+', '', match_json["dire_name"]),
                        match_json["radiant_win"], day, tournament_id
                    ))
                except:
                    print "Failed to add match: %s" % match_json["match_id"]
                    continue

            for key, value in enumerate(picks):
                key = int(key)

                if key <= 5:
                    result_string = "b1"
                elif key <= 9:
                    result_string = "p1"
                    if value["team"] == 0 and radiant_win or value["team"] == 1 and not radiant_win:
                        result_string += "w"
                    else:
                        result_string += "l"
                elif key <= 13:
                    result_string = "b2"
                elif key <= 17:
                    result_string = "p2"
                    if value["team"] == 0 and radiant_win or value["team"] == 1 and not radiant_win:
                        result_string += "w"
                    else:
                        result_string += "l"
                elif key <= 19:
                    result_string = "b3"
                else:
                    result_string = "p3"
                    if value["team"] == 0 and radiant_win or value["team"] == 1 and not radiant_win:
                        result_string += "w"
                    else:
                        result_string += "l"
                print "Match is:", match_json["match_id"]
                session.add(Result(tournament_id, value["hero_id"], int(match_json["match_id"]), result_string,
                                   match_json["start_time"], series_id, (value["team"] == 0)))
    transaction.commit()


def add_matches_guesser(session, tournament_id, tstamp_from):
    match_list_json = get_league_match_list(tournament_id)

    matches = [(match["match_id"], match["series_id"]) for match in match_list_json["result"]["matches"]
               if match["start_time"] > tstamp_from]
    print "matches", matches
    for match, series_id in matches:
        match_json = get_match_details(match)["result"]
        if len(match_json["players"]) < 3:
            continue  # dont count the 1v1s
        for player in match_json["players"]:
            new_hero_game = HeroGame(match, player["hero_id"])
            items = []
            item_value_sum = 0  # we only want to choose/select builds that are guessable (i.e not boots + wand)
            session.add(new_hero_game)
            session.flush()
            empty_items = 0
            legit_items = [79, 81, 90, 96, 98, 100, 104, 201, 202, 203, 204, 205, 106, 193, 194, 110, 112, 114, 116, 117, 119, 121, 123, 125, 127, 133, 135, 139, 141, 143, 145, 147, 149, 151, 152, 154, 160, 158, 156, 164, 166, 168, 170, 172, 174, 196, 176, 206, 208, 210, 231, 226, 235, 249, 250, 252, 263]
            for i in range(6):
                item = player["item_%s" % i]
                if item == 0:
                    empty_items += 1
                items.append(item)
                session.add(ItemBuild(new_hero_game.id, item, i))
            if empty_items > 1 or not any(item for item in items if item in legit_items):
                session.rollback()
                continue
            session.commit()


def main():
    session = make_session()
    #session2 = make_session(False)
    # dreamleague calibration
    add_matches(session, 5627, 1512057853)

if __name__ == "__main__":
    main()
