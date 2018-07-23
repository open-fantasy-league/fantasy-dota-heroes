import time

import datetime
from operator import is_

from fantasydota.lib.constants import SECONDS_IN_12_HOURS, SECONDS_IN_HOUR
from sqlalchemy import and_

from fantasydota.lib.league import game_from_league_id
from fantasydota.models import Hero, TeamHero, LeagueUser, Sale, TeamHeroHistoric


def sell(session, l_user, hero_id, league_id, started=False):
    user_id = l_user.user_id
    game = game_from_league_id(session, league_id)

    user_money = l_user.money

    teamq_hero = session.query(TeamHero).filter(and_(TeamHero.user_id == user_id,
                                                     TeamHero.league == league_id)).filter(TeamHero.reserve.is_(False))
    if l_user.swap_tstamp:
        return {"success": False,
                "message": "You have already made transfers within the last hour"
                           " You cannot make more until this hour period has passed"}

    if teamq_hero.first():
        check_hero = teamq_hero.filter(and_(TeamHero.hero_id == hero_id))
        check_hero_res = check_hero.first()

        if check_hero_res:
            hero_value = session.query(Hero.value).filter(Hero.league == league_id).filter(Hero.id == hero_id).first()[
                0]
            new_credits = round(user_money + hero_value, 1)
            l_user.money = new_credits
            if started:
                if check_hero_res.active:
                    check_hero_res.reserve = 1
                else:
                    check_hero.delete()
            else:
                check_hero.delete()
            session.add(Sale(l_user.id, hero_id, league_id, hero_value, hero_value, False, False))
            return {"success": True, "message": "%s successfully sold" % game.pickee, "action": "sell", "hero": hero_id,
                    "new_credits": new_credits}
        else:
            return {"success": False, "message": "Cannot sell, %s not in your team" % game.pickee}

    return {"success": False, "message": "Erm....you don't appear to be in this league. This is awkward"}


def buy(session, l_user, hero_id, league_id, started=False):
    user_id = l_user.user_id
    game = game_from_league_id(session, league_id)
    hero = session.query(Hero).filter(and_(Hero.id == hero_id,
                                                       Hero.league == league_id)).first()

    teamq = session.query(TeamHero).filter(TeamHero.user_id == user_id).filter(TeamHero.league == league_id)
    teamq_all = teamq.all()
    teamq_hero = teamq.filter(TeamHero.hero_id == hero_id)

    user_money = l_user.money

    if user_money < hero.value:
        return {"success": False, "message": "Insufficient credits"}

    new_credits = round(user_money - hero.value, 1)

    size_limit = game.team_size
    if len([t for t in teamq_all if not t.reserve]) >= size_limit:
        message = "Team is currently full"
        return {"success": False, "message": message}
    teamq_hero_res = teamq_hero.first()
    if teamq_hero_res:
        if teamq_hero_res.reserve:
            teamq_hero_res.reserve = 0
            l_user.money = new_credits
            session.add(Sale(l_user.id, hero_id, league_id, hero.value, hero.value, True, False))
            return {"success": True, "message": "%s successfully purchased" % game.pickee,
                    "action": "buy", "hero": hero_id,
                    "new_credits": new_credits}
        return {"success": False, "message": "%s already in team" % game.pickee}
    elif hero.team and hero.team in [
        session.query(Hero.team).filter(Hero.id == th.hero_id).filter(Hero.league == th.league).first()[0] for th in teamq_all
        ]:
        return {"success": False,
                "message": "You already have a %s from %s in team" % game.pickee}
    else:
        l_user.money = new_credits
        active = not started
        session.add(TeamHero(user_id, hero_id, league_id, hero.value, False, active, hero_name=hero.name))
        session.add(Sale(l_user.id, hero_id, league_id, hero.value, hero.value, True, False))
    return {"success": True, "message": "%s successfully purchased" % game.pickee,
            "action": "buy", "hero": hero_id,
            "new_credits": new_credits}


# def swap_in(session, user_id, hero_id, league_id):
#
#     game = game_from_league_id(session, league_id)
#     hero = session.query(Hero).filter(and_(Hero.id == hero_id,
#                                                        Hero.league == league_id)).first()
#
#     teamq = session.query(TeamHero).filter(TeamHero.user_id == user_id).filter(TeamHero.league == league_id).\
#         filter(TeamHero.reserve.is_(False))
#     teamq_all = teamq.all()
#     teamq_hero = teamq.filter(TeamHero.hero_id == hero_id)
#
#     swap_hero = session.query(TeamHero).filter(TeamHero.user_id == user_id).filter(TeamHero.league == league_id). \
#         filter(TeamHero.hero_id == hero_id).first()
#
#     l_user = session.query(LeagueUser).filter(LeagueUser.user_id == user_id).filter(LeagueUser.league == league_id).first()
#
#     if l_user.swap_tstamp:
#         return {"success": False,
#                 "message": "You have made team swaps within the last 24 hours."
#                            " You cannot make more until this 24 hour period has passed"}
#     user_money = l_user.money
#
#     if user_money < hero.value:
#         return {"success": False,
#                 "message": "Insufficient credits. Move other hero out of team first"}
#
#     new_credits = round(user_money - hero.value, 1)
#
#     if teamq.count() >= 5:
#         message = "Team is currently full. Move other hero out of team first"
#         return {"success": False, "message": message}
#     if teamq_hero.first():
#         return {"success": False, "message": "Hero already in team"}
#     elif hero.team and hero.team in [
#         session.query(Hero.team).filter(Hero.id == th.hero_id).filter(Hero.league == th.league).first()[0] for th in teamq_all
#         ]:
#         return {"success": False,
#                 "message": "You already have a %s from %s in main team" % (game.pickee, hero.team)}
#     else:
#         l_user.money = new_credits
#         swap_hero.reserve = False
#         l_user.last_change = int(time.time())
#         session.add(Sale(l_user.id, hero_id, league_id, hero.value, hero.value, True, True))
#     return {"success": True, "message": "Hero successfully Added",
#             "action": "buy", "hero": hero_id,
#             "new_credits": new_credits}
#
#
# def swap_out(session, user_id, hero_id, league_id):
#     l_user = session.query(LeagueUser).filter(LeagueUser.user_id == user_id).filter(LeagueUser.league == league_id).first()
#     if l_user.swap_tstamp:
#         return {"success": False,
#                 "message": "You have made team swaps within the last 24 hours."
#                            " You cannot make more until this 24 hour period has passed"}
#     user_money = l_user.money
#
#     teamq_hero = session.query(TeamHero).filter(and_(TeamHero.user_id == user_id,
#                                                      TeamHero.league == league_id))
#     if teamq_hero.first():
#         check_hero = teamq_hero.filter(and_(TeamHero.hero_id == hero_id))
#         check_hero_res = check_hero.first()
#
#         if check_hero_res:
#             hero_value = session.query(Hero.value).filter(Hero.league == league_id).filter(Hero.id == hero_id).first()[0]
#             new_credits = round(user_money + hero_value, 1)
#             l_user.money = new_credits
#             check_hero_res.reserve = 1
#             l_user.last_change = int(time.time())
#             session.add(Sale(l_user.id, hero_id, league_id, hero_value, hero_value, False, True))
#             return {"success": True, "message": "Hero successfully sold", "action": "sell", "hero": hero_id,
#                     "new_credits": new_credits}
#         else:
#             return {"success": False, "message": "Cannot sell, hero not in your team"}
#
#     return {"success": False, "message": "Erm....you don't appear to be in this league. This is awkward"}


def get_swap_timestamp():
    # swap_at = datetime.datetime.now()
    # swap_at += datetime.timedelta(hours=23)
    # swap_at.replace(minute=59)
    # return time.mktime(swap_at.timetuple())
    return time.time() + SECONDS_IN_HOUR
