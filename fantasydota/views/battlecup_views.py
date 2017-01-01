from fantasydota.lib.trade import sell, buy
from pyramid.httpexceptions import HTTPForbidden
from pyramid.security import authenticated_userid
from pyramid.view import view_config

from fantasydota import DBSession
from fantasydota.models import BattlecupUser, League, Hero, TeamHero, BattlecupTeamHeroHistory, Battlecup, \
    BattlecupRound, BattlecupUserRound
from sqlalchemy import and_
from sqlalchemy import func


@view_config(route_name='battlecup', renderer='../templates/battlecup.mako')
def battlecup(request):
    session = DBSession()
    user = authenticated_userid(request)
    transfer_open = False

    league_id = int(request.params.get("league")) if request.params.get("league") else None \
        or request.registry.settings["default_league"]
    battlecup_id = int(request.params.get("battlecup_id")) if request.params.get("battlecup_id") else None \
                                                                                       or -1
    print "b IDIDIDID", battlecup_id
    league = session.query(League).filter(League.id == league_id).first()
    is_playing = True

    all_bcup_user = [x[0] for x in session.query(BattlecupUser.battlecup).filter(BattlecupUser.username == user)]
    all_bcups = session.query(Battlecup).filter(Battlecup.id.in_(all_bcup_user)).all()#[::-1]  # reversed

    if league.battlecup_status == 0:
        class FakeBcup(object):
            def __init__(self, id, day):
                self.day = day
                self.id = id

        fake_bcup = FakeBcup(-1, league.current_day) # fake because hasnt been created until transfer window closes
        all_bcups.append(fake_bcup)
    transfer_open = True if battlecup_id == -1 and league.battlecup_status == 0 else False
    return_dict = {"league": league, "is_playing": is_playing, "battlecup_id": battlecup_id,
                   "transfer_open": transfer_open, "all_bcups": all_bcups}

    heroes = session.query(Hero).filter(and_(Hero.league == league_id, Hero.is_battlecup.is_(True))).all()
    return_dict["heroes"] = heroes

    # TODO if its not todays need to query historic bcup stuff
    team_ids = [res[0] for res in session.query(TeamHero.hero_id). \
        filter(and_(TeamHero.user == user, TeamHero.league == league_id,
                    TeamHero.is_battlecup.is_(True))).all()]
    print team_ids
    team = session.query(Hero).filter(and_(Hero.id.in_(team_ids),
                                           Hero.is_battlecup.is_(True),
                                           Hero.league == league_id)).all()
    print team
    return_dict["team"] = team

        #userq = session.query(BattlecupUser).filter(and_(Hero.league == league_id))
    # if not user:
    #     battlecup_id = 1
    #     is_playing = False
    # else:
    #     battlecup_id = request.params.get("battlecup_id")
    #     if not battlecup_id:
    #         battlecupq = session.query(BattlecupUser.battlecup_id).filter(BattlecupUser.username == user).first()
    #         if battlecupq:
    #             battlecup_id = battlecupq[0]
    #         else:
    #             is_playing = False
    #             battlecup_id = 1
    return return_dict


@view_config(route_name="sell_hero_battlecup", renderer="json")
def sell_hero_battlecup(request):
    session = DBSession()
    user = authenticated_userid(request)
    if user is None:
        raise HTTPForbidden()

    hero_id = request.POST["hero"]
    # transfer_think_open = request.POST["transfer"] really doesnt matter what the user thinks! :D
    league_id = request.POST["league"]

    transfer_open = True
    # transfer_think_open = request.POST["transfer"] really doesnt matter what the user thinks! :D
    if not transfer_open:
        return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    return sell(session, user, hero_id, league_id, True)


@view_config(route_name="buy_hero_battlecup", renderer="json")
def buy_hero_battlecup(request):
    session = DBSession()
    user = authenticated_userid(request)
    if user is None:
        raise HTTPForbidden()

    hero_id = int(request.POST["hero"])
    league_id = request.POST["league"]
    transfer_open = True
    # transfer_think_open = request.POST["transfer"] really doesnt matter what the user thinks! :D
    if not transfer_open:
        return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    return buy(session, user, hero_id, league_id, True)


@view_config(route_name="battlecup_add_league_team", renderer="json")
def battlecup_add_league_team(request):
    session = DBSession()
    user = authenticated_userid(request)
    if user is None:
        raise HTTPForbidden()
    league_id = request.POST["league"]

    # first nuke current team
    session.query(TeamHero).filter(and_(TeamHero.league == league_id,
                                        TeamHero.is_battlecup.is_(True),
                                        TeamHero.user == user)).delete()

    league_team = session.query(TeamHero).filter(and_(TeamHero.league == league_id,
                                                      TeamHero.is_battlecup.is_(False),
                                                      TeamHero.user == user)).all()
    heroes_to_add = []
    money = 50
    message = "League team successfully chosen"
    for hero in league_team:
        new_h = session.query(Hero).filter(and_(Hero.league == league_id,
                                                Hero.is_battlecup.is_(True),
                                                Hero.id == hero.hero_id)).first()
        money -= new_h.value
        if money > 0:
            heroes_to_add.append(new_h.id)
            session.add(TeamHero(user, new_h.id, league_id, True))
        else:
            message = "League team too expensive for battlecup values. Hero removed"
            money += new_h.value
    return {"success": True, "message": message, "heroes": heroes_to_add, "new_credits": round(money, 1)}


@view_config(route_name="battlecup_add_yesterday_team", renderer="json")
def battlecup_add_yesterday_team(request):
    session = DBSession()
    user = authenticated_userid(request)
    if user is None:
        raise HTTPForbidden()
    league_id = request.POST["league"]
    yesterday = session.query(League.current_day).filter(League.id == league_id).first()[0] - 1
    if yesterday < 0:
        return {"success": False, "message": "No previous day to select from"}

    # first nuke current team
    session.query(TeamHero).filter(and_(TeamHero.league == league_id,
                                        TeamHero.is_battlecup.is_(True),
                                        TeamHero.user == user)).delete()

    yesterday_team = session.query(BattlecupTeamHeroHistory).filter(and_(BattlecupTeamHeroHistory.league == league_id,
                                                                      BattlecupTeamHeroHistory.user == user,
                                                                      BattlecupTeamHeroHistory.day == yesterday)).all()
    heroes_to_add = []
    money = 50
    message = "Yesterday's team successfully chosen"
    for hero in yesterday_team:
        new_h = session.query(Hero).filter(and_(Hero.league == league_id,
                                                Hero.is_battlecup.is_(True),
                                                Hero.id == hero.hero_id)).first()
        money -= new_h.value
        if money > 0:
            heroes_to_add.append(new_h.id)
            session.add(TeamHero(user, new_h.id, league_id, True))
        else:
            message = "Yesterday's team too expensive for battlecup values. Hero removed"
            money += new_h.value
    return {"success": True, "message": message, "heroes": heroes_to_add, "new_credits": round(money, 1)}


# @view_config(route_name='battlecup_team', renderer='templates/battlecup_team.mako')
# def battlecup_team(request):
#     session = DBSession()
#     user = authenticated_userid(request)
#     league_id = int(request.params.get("league")) if request.params.get("league") else None \
#         or request.registry.settings["default_league"]
#     league = session.query(League).filter(League.id == league_id).first()
#     is_playing = True
#     if not user:
#         battlecup_id = 1
#         is_playing = False
#     else:
#         battlecup_id = request.params.get("battlecup_id")
#         if not battlecup_id:
#             battlecupq = session.query(BattlecupUser.battlecup_id).filter(BattlecupUser.username == user).first()
#             if battlecupq:
#                 battlecup_id = battlecupq[0]
#             else:
#                 is_playing = False
#                 battlecup_id = 1
#     return {"league": league, "battlecup_id": battlecup_id, "is_playing": is_playing}


@view_config(route_name='battlecup_json', renderer='json')
def battlecup_json(request):

    # Hack to have a bye for the missing 8th player
    session = DBSession()
    battlecup_id = int(request.params.get("battlecup_id"))
    league_id = int(request.params.get("league"))

    battlecup = session.query(Battlecup).filter(Battlecup.id == battlecup_id).first()
    print "Battlecup", battlecup.current_round
    match_count = 2**(battlecup.total_rounds - 1)
    player_names, hero_imgs, results = [(None, None) for _ in xrange(match_count)], [], []
    bcup_round_one = session.query(BattlecupRound).filter(and_(BattlecupRound.battlecup == battlecup_id,
                                                               BattlecupRound.round_ == 1)).\
        order_by(BattlecupRound.id).all()

    bcup_round_two = session.query(BattlecupRound).filter(and_(BattlecupRound.battlecup == battlecup_id,
                                                               BattlecupRound.round_ == 2)). \
        order_by(BattlecupRound.id).all()

    bcup_round_three = session.query(BattlecupRound).filter(and_(BattlecupRound.battlecup == battlecup_id,
                                                               BattlecupRound.round_ == 3)). \
        order_by(BattlecupRound.id).all()

    bcup_round_four = session.query(BattlecupRound).filter(and_(BattlecupRound.battlecup == battlecup_id,
                                                               BattlecupRound.round_ == 4)). \
        order_by(BattlecupRound.id).all()

    results_full, round_one_results, round_two_results, round_three_results, round_four_results = \
        [], [], [], [], []
    for i, round_ in enumerate(bcup_round_one):
        player_names[i] = (round_.player_one, round_.player_two)

        p1_heroes = {"pname": round_.player_one,
                     "heroes": [
                         x[0] for x in session.query(TeamHero.hero_name).
                         filter(and_(TeamHero.league == league_id,
                                     TeamHero.is_battlecup.is_(True),
                                     TeamHero.user == round_.player_one)).all()
                         ]}

        p2_heroes = {"pname": round_.player_two,
                     "heroes": [
                         x[0] for x in session.query(TeamHero.hero_name).
                         filter(and_(TeamHero.league == league_id,
                                     TeamHero.is_battlecup.is_(True),
                                     TeamHero.user == round_.player_two)).all()
                         ]}

        hero_imgs.extend([p1_heroes, p2_heroes])

        if battlecup.current_round > 1:
            print "round_.player_one: ", round_.player_one
            print "round_.id: ", round_.id
            p1_points = session.query(BattlecupUserRound.points).filter(and_(BattlecupUserRound.battlecupround == round_.id,
                                                                      BattlecupUserRound.username == round_.player_one))\
                .first()[0]

            p2_points = session.query(BattlecupUserRound.points).filter(and_(BattlecupUserRound.battlecupround == round_.id,
                                                                             BattlecupUserRound.username == round_.player_two)) \
                .first()

            if p2_points:  # If its none leave it as none, this is a bye
                p2_points = p2_points[0]

            round_one_results.append([p1_points, p2_points])
    results_full.append(round_one_results)
    if battlecup.current_round > 2:
        for round_ in bcup_round_two:
            p1_points = session.query(BattlecupUserRound.points).filter(and_(BattlecupUserRound.battlecupround == round_.id,
                                                                      BattlecupUserRound.username == round_.player_one))\
                .first()[0]

            p2_points = session.query(BattlecupUserRound.points).filter(and_(BattlecupUserRound.battlecupround == round_.id,
                                                                             BattlecupUserRound.username == round_.player_two)) \
                .first()[0]

            round_two_results.append([p1_points, p2_points])
    results_full.append(round_two_results)

    if battlecup.current_round > 3:
        for round_ in bcup_round_three:
            p1_points = session.query(BattlecupUserRound.points).filter(and_(BattlecupUserRound.battlecupround == round_.id,
                                                                      BattlecupUserRound.username == round_.player_one))\
                .first()[0]

            p2_points = session.query(BattlecupUserRound.points).filter(and_(BattlecupUserRound.battlecupround == round_.id,
                                                                             BattlecupUserRound.username == round_.player_two)) \
                .first()[0]

            round_three_results.append([p1_points, p2_points])
    results_full.append(round_three_results)

    if battlecup.current_round > 4:
        for round_ in bcup_round_four:
            p1_points = session.query(BattlecupUserRound.points).filter(and_(BattlecupUserRound.battlecupround == round_.id,
                                                                      BattlecupUserRound.username == round_.player_one))\
                .first()[0]

            p2_points = session.query(BattlecupUserRound.points).filter(and_(BattlecupUserRound.battlecupround == round_.id,
                                                                             BattlecupUserRound.username == round_.player_two)) \
                .first()[0]

            round_four_results.append([p1_points, p2_points])
    results_full.append(round_four_results)

    bracket_dict = {
        "teams": player_names,
        "results": results_full
    }

    return {"bracket_dict": bracket_dict, "hero_imgs": hero_imgs}
