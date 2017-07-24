from sqlalchemy import and_

from fantasydota.models import League, Hero, TeamHero, LeagueUser, Sale


def sell(session, user_id, hero_id, league_id):
    transfer_actually_open = session.query(League.transfer_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    l_user = session.query(LeagueUser).filter(LeagueUser.user_id == user_id).first()

    teamq = session.query(TeamHero).filter(and_(TeamHero.user_id == user_id,
                                                        TeamHero.league == league_id))

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
            check_hero.delete()
            session.add(Sale(l_user.id, hero_id, league_id, hero_value, hero_value, False))
            return {"success": True, "message": "Hero successfully sold", "action": "sell", "hero": hero_id,
                    "new_credits": new_credits}
        else:
            return {"success": False, "message": "ERROR: Cannot sell, hero not in your team"}

    return {"success": False, "message": "Erm....you don't appear to be in this league. This is awkward"}


def buy(session, user_id, hero_id, league_id):
    transfer_actually_open = session.query(League.transfer_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    hero_value = session.query(Hero.value).filter(and_(Hero.id == hero_id,
                                                       Hero.league == league_id)).first()[0]

    teamq = session.query(TeamHero).filter(TeamHero.user_id == user_id).filter(TeamHero.league == league_id)
    teamq_hero = teamq.filter(TeamHero.hero_id == hero_id)

    l_user = session.query(LeagueUser).filter(LeagueUser.user_id == user_id).filter(LeagueUser.league == league_id).first()

    user_money = l_user.money

    if user_money < hero_value:
        return {"success": False, "message": "ERROR: Insufficient credits"}

    new_credits = round(user_money - hero_value, 1)

    if teamq.count() >= 5:
        return {"success": False, "message": "ERROR: Team is currently full"}
    if teamq_hero.first():
        return {"success": False, "message": "ERROR: Hero already in team"}
    else:
        l_user.money = new_credits
        session.add(TeamHero(user_id, hero_id, league_id, hero_value))
        session.add(Sale(l_user.id, hero_id, league_id, hero_value, hero_value, True))
    return {"success": True, "message": "Hero successfully purchased",
            "action": "buy", "hero": hero_id,
            "new_credits": new_credits}