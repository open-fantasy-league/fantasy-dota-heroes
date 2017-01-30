from fantasydota.lib.battlecup import player_hero_imgs
from fantasydota.lib.trade import sell, buy
from pyramid.httpexceptions import HTTPForbidden, HTTPFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config

from fantasydota import DBSession
from fantasydota.models import BattlecupUser, League, Hero, TeamHero, BattlecupTeamHeroHistory, Battlecup, \
    BattlecupRound, BattlecupUserRound, User
from sqlalchemy import and_
from sqlalchemy import func


@view_config(route_name='battlecup', renderer='../templates/battlecup.mako')
def battlecup(request):
    session = DBSession()
    user_id = authenticated_userid(request)

    if not user_id:
        return HTTPFound('/login')

    league_id = int(request.params.get("league", request.registry.settings["default_league"]))
    battlecup_id = int(request.params.get("battlecup_id", -1))
    league = session.query(League).filter(League.id == league_id).first()
    is_playing = True

    all_bcup_user = session.query(BattlecupUser).filter(BattlecupUser.user_id == user_id).all()
    all_bcups = session.query(Battlecup).filter(Battlecup.id.in_([x.battlecup for x in all_bcup_user])).all()

    class FakeBcup(object):
        def __init__(self, id, day):
            self.day = day
            self.id = id

    if league.battlecup_status == 0:
        fake_bcup = FakeBcup(-1, league.current_day)  # fake because hasnt been created until transfer window closes
        all_bcups.append(fake_bcup)
    transfer_open = True if battlecup_id == -1 and league.battlecup_status == 0 else False
    return_dict = {"league": league, "is_playing": is_playing,
                   "transfer_open": transfer_open, "all_bcups": all_bcups}

    if battlecup_id != -1:
        return_dict["battlecup"] = session.query(Battlecup).filter(Battlecup.id == battlecup_id).first()
    else:
        today = [bcup for bcup in all_bcups if bcup.day == league.current_day]
        if today:
            return_dict["battlecup"] = today[0]
        else:
            return_dict["battlecup"] = FakeBcup(-1, league.current_day)  # we are not entered into any today

    heroes = session.query(Hero).filter(and_(Hero.league == league_id, Hero.is_battlecup.is_(True))).all()
    return_dict["heroes"] = heroes

    # TODO if its not todays need to query historic bcup stuff
    team_ids = [res[0] for res in session.query(TeamHero.hero_id). \
        filter(and_(TeamHero.user_id == user_id, TeamHero.league == league_id,
                    TeamHero.is_battlecup.is_(True))).all()]
    team = session.query(Hero).filter(and_(Hero.id.in_(team_ids),
                                           Hero.is_battlecup.is_(True),
                                           Hero.league == league_id)).all()
    return_dict["team"] = team

    return return_dict


@view_config(route_name="sell_hero_battlecup", renderer="json")
def sell_hero_battlecup(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        raise HTTPForbidden()

    hero_id = request.POST["hero"]
    # transfer_think_open = request.POST["transfer"] really doesnt matter what the user thinks! :D
    league_id = request.POST["league"]

    transfer_open = True
    # transfer_think_open = request.POST["transfer"] really doesnt matter what the user thinks! :D
    if not transfer_open:
        return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    return sell(session, user_id, hero_id, league_id, True)


@view_config(route_name="buy_hero_battlecup", renderer="json")
def buy_hero_battlecup(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        raise HTTPForbidden()

    hero_id = int(request.POST["hero"])
    league_id = request.POST["league"]
    transfer_open = True
    # transfer_think_open = request.POST["transfer"] really doesnt matter what the user thinks! :D
    if not transfer_open:
        return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    return buy(session, user_id, hero_id, league_id, True)


@view_config(route_name="battlecup_add_league_team", renderer="json")
def battlecup_add_league_team(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        raise HTTPForbidden()
    league_id = request.POST["league"]

    # first nuke current team
    session.query(TeamHero).filter(and_(TeamHero.league == league_id,
                                        TeamHero.is_battlecup.is_(True),
                                        TeamHero.user_id == user_id)).delete()

    league_team = session.query(TeamHero).filter(and_(TeamHero.league == league_id,
                                                      TeamHero.is_battlecup.is_(False),
                                                      TeamHero.user_id == user_id)).all()
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
            session.add(TeamHero(user_id, new_h.id, league_id, True, 1, 0))
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


@view_config(route_name='battlecup_json', renderer='json')
def battlecup_json(request):

    # Hack to have a bye for the missing 8th player
    session = DBSession()
    battlecup_id = int(request.params.get("battlecup_id"))
    league_id = int(request.params.get("league"))

    battlecup = session.query(Battlecup).filter(Battlecup.id == battlecup_id).first()
    if battlecup.day != session.query(League.current_day).filter(League.id == league_id).scalar():
        old_hero = True
    else:
        old_hero = False
    match_count = 2**(battlecup.total_rounds - 1)
    player_names, hero_imgs, results = [(None, None) for _ in xrange(match_count)], [], []

    for current_round in range(1, battlecup.total_rounds + 1):
        bcup_rounds = session.query(BattlecupRound).filter(and_(BattlecupRound.battlecup == battlecup_id,
                                                               BattlecupRound.round_ == current_round)).\
            order_by(BattlecupRound.id).all()
        round_results = []
        for i, round_ in enumerate(bcup_rounds):
            if current_round == 1:
                player_one_name = session.query(User.username).filter(User.id == round_.player_one).first()\
                                  or [None]
                player_two_name = session.query(User.username).filter(User.id == round_.player_two).first()\
                                  or [None]
                player_names[i] = (player_one_name[0], player_two_name[0])
                hero_imgs.extend(player_hero_imgs(session, battlecup, round_, league_id, old_hero))

            if battlecup.current_round > current_round:  # if round has ended and we've started next round
                p1_points = \
                session.query(BattlecupUserRound.points).filter(and_(BattlecupUserRound.battlecupround == round_.id,
                                                                     BattlecupUserRound.user_id == round_.player_one)) \
                    .first()[0]

                p2_points = session.query(BattlecupUserRound.points).filter(
                    and_(BattlecupUserRound.battlecupround == round_.id,
                         BattlecupUserRound.user_id == round_.player_two)) \
                    .first()

                if p2_points:  # If its none leave it as none, this is a bye
                    p2_points = p2_points[0]

                round_results.append([p1_points, p2_points])
        results.append(round_results)

    bracket_dict = {
        "teams": player_names,
        "results": results
    }

    return {"bracket_dict": bracket_dict, "hero_imgs": hero_imgs}
