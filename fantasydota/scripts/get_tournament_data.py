import json
import os
import urllib2

import time
import transaction

from fantasydota.lib.session_utils import make_session
from fantasydota.models import Result, HeroGame, ItemBuild, Match, League

APIKEY = os.environ.get("APIKEY")
if not APIKEY:
    print "Set your APIKEY environment variable"


def dont_piss_off_valve_but_account_for_sporadic_failures(req_url):
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
        "https://api.stratz.com/api/v1/match?leagueId=%s&take=9001" % league_id)


def get_match_details(match_id):
    return dont_piss_off_valve_but_account_for_sporadic_failures(
        "https://api.stratz.com/api/v1/match?matchId=%s&include=Team,pickban,player" % match_id)


def add_matches(session, tournament_id, tstamp_from=0):
    match_list_json = get_league_match_list(tournament_id)

    matches = [(match["id"], match.get("series", {"id": match["id"]})["id"]) for match in match_list_json["results"]
               if match["endDate"] > tstamp_from]
    print "matches", matches
    for match, series_id in matches:
        with transaction.manager:
            if session.query(Result).filter(Result.match_id == match).first():  # if old result dont process
                continue

            match_json = get_match_details(match)["results"][0]
            print "Match is:", match_json["id"]
            radiant_win = match_json["didRadiantWin"]
            try:
                picks = match_json["pickBans"]
            except KeyError:  # game crashed and they remade with all pick. need to manually
                print "MatchID: %s no picks and bans. Need manually inserting" % match
                continue
            if len(picks) < 16:  # theres some weird buggy matches in there
                print "MatchID: %s fucked up picks bans. Check if should be added" % match
                continue
            elif len(picks) < 20:
                print "MatchID: %s fucked up picks bans. not 20. Check if need update" % match
                continue
            day = session.query(League.current_day).filter(League.id == tournament_id).first()
            if not day:
                print "No day. are you calibrating?"
                day = 0
            try:
                session.add(Match(
                    int(match_json["id"]), match_json["radiantTeam"]["name"], match_json["direTeam"]["name"],
                    radiant_win, day
                ))
            except KeyError:
                session.add(Match(
                    int(match_json["id"]), "No name", "No name",
                    radiant_win, day
                ))

            for key, value in enumerate(picks):
                key = int(key)

                if key <= 3:
                    result_string = "b1"
                elif key <= 7:
                    result_string = "p1"
                    if value["team"] == 0 and radiant_win or value["team"] == 1 and not radiant_win:
                        result_string += "w"
                    else:
                        result_string += "l"
                elif key <= 11:
                    result_string = "b2"
                elif key <= 15:
                    result_string = "p2"
                    if value["team"] == 0 and radiant_win or value["team"] == 1 and not radiant_win:
                        result_string += "w"
                    else:
                        result_string += "l"
                elif key <= 17:
                    result_string = "b3"
                else:
                    result_string = "p3"
                    if value["team"] == 0 and radiant_win or value["team"] == 1 and not radiant_win:
                        result_string += "w"
                    else:
                        result_string += "l"
                session.add(Result(tournament_id, value["heroId"], int(match_json["id"]), result_string,
                                   match_json["endDate"], series_id, (value["team"] == 0)))
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
            if empty_items > 1 or any(item for item in items if item in legit_items):
                session.rollback()
                continue
            session.commit()


def main():
    session = make_session()
    #add_matches_guesser(session2, 5197, 1489449600)
    # for calibration for esl genting
    # add_matches(session, 5504, 0)
    # add_matches(session, 5401, 0)
    # add_matches(session, 5336, 0)
    # add_matches(session, 5434, 0)
    # add_matches(session, 5388, 0)
    # add_matches(session, 5227, 0)
    # add_matches(session, 4665, 0)
    add_matches(session, 5353, 1496537374)
    add_matches(session, 5157, 1492994974)

    #add_matches(session, 5401, 1500121359)  # TI7. games are qualifiers
    #add_matches(session, 4682, t)  # https://www.dotabuff.com/esports/leagues/4665

if __name__ == "__main__":
    main()