from fantasydota.models import League, Hero, LeagueUser, TeamHero
from sqlalchemy import and_


def sell(session, user_id, hero_id, league_id, is_battlecup):
    transfer_actually_open = session.query(League.transfer_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    hero_value = session.query(Hero.value).filter(and_(Hero.id == hero_id,
                                                       Hero.is_battlecup.is_(is_battlecup),
                                                       Hero.league == league_id)).first()[0]
    teamq = session.query(TeamHero.hero_id).filter(and_(TeamHero.user_id == user_id,
                                                TeamHero.league == league_id,
                                                TeamHero.is_battlecup.is_(is_battlecup)))
    user_money = 50.0 - sum([hero.value for hero in
                             session.query(Hero).filter(and_(Hero.is_battlecup.is_(is_battlecup),
                                                             Hero.league == league_id,
                                                             Hero.id.in_([x[0] for x in teamq.all()])))
                             ])

    new_credits = round(user_money + hero_value, 1)

    teamq_hero = session.query(TeamHero).filter(and_(TeamHero.user_id == user_id,
                                                     TeamHero.is_battlecup.is_(is_battlecup),
                                                     TeamHero.league == league_id))
    if teamq_hero.first():
        check_hero = teamq_hero.filter(and_(TeamHero.hero_id == hero_id, TeamHero.is_battlecup.is_(is_battlecup)))
        check_hero_res = check_hero.first()

        if check_hero_res:
            if check_hero_res.active:
                return {"success": False, "message": "Cannot sell before loan period ended"}

            check_hero.delete()
            return {"success": True, "message": "Hero successfully sold", "action": "sell", "hero": hero_id,
                    "new_credits": new_credits}
        else:
            return {"success": False, "message": "ERROR: Cannot sell, hero not in your team"}

    return {"success": False, "message": "Erm....you don't appear to be in this league. This is awkward"}


def buy(session, user_id, hero_id, league_id, is_battlecup, days):
    transfer_actually_open = session.query(League.transfer_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    hero_value = session.query(Hero.value).filter(and_(Hero.id == hero_id,
                                                       Hero.league == league_id,
                                                       Hero.is_battlecup.is_(is_battlecup))).first()[0]

    teamq = session.query(TeamHero).filter(TeamHero.user_id == user_id).filter(TeamHero.league == league_id).\
                                                filter(TeamHero.is_battlecup.is_(is_battlecup))
    teamq_hero = teamq.filter(TeamHero.hero_id == hero_id)

    user_money = 50.0 - sum([hero.value for hero in
                             session.query(Hero).filter(and_(Hero.is_battlecup.is_(is_battlecup),
                                                             Hero.league == league_id,
                                                             Hero.id.in_([x.hero_id for x in teamq.all()])))
                             ])

    if user_money < hero_value:
        return {"success": False, "message": "ERROR: Insufficient credits"}

    new_credits = round(user_money - hero_value, 1)

    if teamq.count() >= 5:
        return {"success": False, "message": "ERROR: Team is currently full"}
    if teamq_hero.first():
        return {"success": False, "message": "ERROR: Hero already in team"}
    else:
        cost = round(hero_value * (1 - (0.015 * (days - 1))), 1)  # knock off 1.5% for every extra game day loaned for
        session.add(TeamHero(user_id, hero_id, league_id, is_battlecup, days, cost))
    return {"success": True, "message": "Hero successfully loaned for %s days" % days,
            "action": "buy", "hero": hero_id,
            "new_credits": new_credits}