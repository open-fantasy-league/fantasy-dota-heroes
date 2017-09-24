from sqlalchemy import and_

from fantasydota.models import League, Hero, TeamHero, LeagueUser, Sale


def sell(session, user_id, hero_id, league_id, reserve):
    l_user = session.query(LeagueUser).filter(LeagueUser.user_id == user_id).filter(LeagueUser.league == league_id).first()

    user_money = l_user.reserve_money if reserve else l_user.money

    teamq_hero = session.query(TeamHero).filter(and_(TeamHero.user_id == user_id,
                                                     TeamHero.league == league_id)).filter(TeamHero.reserve.is_(reserve))
    if teamq_hero.first():
        check_hero = teamq_hero.filter(and_(TeamHero.hero_id == hero_id))
        check_hero_res = check_hero.first()

        if check_hero_res:
            hero_value = session.query(Hero.value).filter(Hero.league == league_id).filter(Hero.id == hero_id).first()[0]
            new_credits = round(user_money + hero_value, 1)
            if reserve:
                l_user.reserve_money = new_credits
            else:
                l_user.money = new_credits
            check_hero.delete()
            session.add(Sale(l_user.id, hero_id, league_id, hero_value, hero_value, False))
            return {"success": True, "message": "Hero successfully sold", "action": "sell", "hero": hero_id,
                    "new_credits": new_credits}
        else:
            return {"success": False, "message": "ERROR: Cannot sell, hero not in your team"}

    return {"success": False, "message": "Erm....you don't appear to be in this league. This is awkward"}


def buy(session, user_id, hero_id, league_id, reserve):

    hero_value = session.query(Hero.value).filter(and_(Hero.id == hero_id,
                                                       Hero.league == league_id)).first()[0]

    teamq = session.query(TeamHero).filter(TeamHero.user_id == user_id).filter(TeamHero.league == league_id).\
        filter(TeamHero.reserve.is_(reserve))
    teamq_hero = teamq.filter(TeamHero.hero_id == hero_id)

    l_user = session.query(LeagueUser).filter(LeagueUser.user_id == user_id).filter(LeagueUser.league == league_id).first()

    user_money = l_user.reserve_money if reserve else l_user.money

    if user_money < hero_value:
        return {"success": False, "message": "ERROR: Insufficient credits"}

    new_credits = round(user_money - hero_value, 1)

    if teamq.count() >= 5:
        message = "ERROR: Reserves currently full" if reserve else "ERROR: Team is currently full"
        return {"success": False, "message": message}
    if teamq_hero.first():
        return {"success": False, "message": "ERROR: Hero already in %steam" % ("reserve " if reserve else "")}
    elif session.query(TeamHero).filter(TeamHero.user_id == user_id).filter(TeamHero.league == league_id). \
            filter(TeamHero.reserve.is_(not reserve)).filter(TeamHero.hero_id == hero_id).first():
        return {"success": False, "message": "ERROR: Hero already in %steam" % ("reserve " if reserve else "")}
    else:
        if reserve:
            l_user.reserve_money = new_credits
        else:
            l_user.money = new_credits
        session.add(TeamHero(user_id, hero_id, league_id, hero_value, reserve))
        session.add(Sale(l_user.id, hero_id, league_id, hero_value, hero_value, True))
    return {"success": True, "message": "Hero successfully purchased",
            "action": "buy", "hero": hero_id,
            "new_credits": new_credits}


def swap_in(session, user_id, hero_id, league_id):

    hero_value = session.query(Hero.value).filter(and_(Hero.id == hero_id,
                                                       Hero.league == league_id)).first()[0]

    teamq = session.query(TeamHero).filter(TeamHero.user_id == user_id).filter(TeamHero.league == league_id).\
        filter(TeamHero.reserve.is_(False))
    teamq_hero = teamq.filter(TeamHero.hero_id == hero_id)

    swap_hero = session.query(TeamHero).filter(TeamHero.user_id == user_id).filter(TeamHero.league == league_id). \
        filter(TeamHero.hero_id == hero_id).first()

    l_user = session.query(LeagueUser).filter(LeagueUser.user_id == user_id).filter(LeagueUser.league == league_id).first()

    user_money = l_user.money

    if user_money < hero_value:
        return {"success": False,
                "message": "ERROR: Insufficient credits. Move other hero out of team first"}

    new_credits = round(user_money - hero_value, 1)

    if teamq.count() >= 5:
        message = "ERROR: Team is currently full. Move other hero out of team first"
        return {"success": False, "message": message}
    if teamq_hero.first():
        return {"success": False, "message": "ERROR: Hero already in team"}
    else:
        l_user.money = new_credits
        swap_hero.reserve = False
    return {"success": True, "message": "Hero successfully Added",
            "action": "buy", "hero": hero_id,
            "new_credits": new_credits}


def swap_out(session, user_id, hero_id, league_id):
    l_user = session.query(LeagueUser).filter(LeagueUser.user_id == user_id).filter(LeagueUser.league == league_id).first()

    user_money = l_user.money

    teamq_hero = session.query(TeamHero).filter(and_(TeamHero.user_id == user_id,
                                                     TeamHero.league == league_id))
    if teamq_hero.first():
        check_hero = teamq_hero.filter(and_(TeamHero.hero_id == hero_id))
        check_hero_res = check_hero.first()

        if check_hero_res:
            hero_value = session.query(Hero.value).filter(Hero.league == league_id).filter(Hero.id == hero_id).first()[0]
            new_credits = round(user_money + hero_value, 1)
            l_user.money = new_credits
            check_hero_res.reserve = 1
            return {"success": True, "message": "Hero successfully sold", "action": "sell", "hero": hero_id,
                    "new_credits": new_credits}
        else:
            return {"success": False, "message": "ERROR: Cannot sell, hero not in your team"}

    return {"success": False, "message": "Erm....you don't appear to be in this league. This is awkward"}
