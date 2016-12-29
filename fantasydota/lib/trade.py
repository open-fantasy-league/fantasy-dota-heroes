from fantasydota.models import League, Hero, LeagueUser, TeamHero
from sqlalchemy import and_


def sell(session, user, hero_id, league_id, is_battlecup):
    transfer_actually_open = session.query(League.transfer_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    hero_value = session.query(Hero.value).filter(and_(Hero.id == hero_id,
                                                       Hero.is_battlecup.is_(is_battlecup),
                                                       Hero.league == league_id)).first()[0]
    if is_battlecup:
        teamq = session.query(TeamHero.hero_id).filter(and_(TeamHero.user == user,
                                                    TeamHero.league == league_id,
                                                    TeamHero.is_battlecup.is_(is_battlecup)))
        user_money = 50.0 - sum([hero.value for hero in
                                 session.query(Hero).filter(and_(Hero.is_battlecup == True,
                                                                 Hero.league == league_id,
                                                                 Hero.id.in_([x[0] for x in teamq.all()])))
                                 ])
    else:
        user_money_q = session.query(LeagueUser.money).filter(and_(LeagueUser.username == user,
                                                               LeagueUser.league == league_id))
        user_money = user_money_q.first()[0]

    new_credits = round(user_money + hero_value, 1)

    teamq_hero = session.query(TeamHero).filter(and_(TeamHero.user == user,
                                                     TeamHero.is_battlecup.is_(is_battlecup),
                                                     TeamHero.league == league_id))
    if teamq_hero.first():
        check_hero = teamq_hero.filter(and_(TeamHero.hero_id == hero_id, TeamHero.is_battlecup.is_(is_battlecup)))

        if check_hero.first():
            check_hero.delete()
            if not is_battlecup:
                user_money_q.update({LeagueUser.money: new_credits})
            return {"success": True, "message": "Hero successfully sold", "action": "sell", "hero": hero_id,
                    "new_credits": new_credits}
        else:
            return {"success": False, "message": "ERROR: Hero is not in your team to sell"}

    return {"success": False, "message": "Erm....you don't appear to be in this league. This is awkward"}


def buy(session, user, hero_id, league_id, is_battlecup):


    hero_value = session.query(Hero.value).filter(and_(Hero.id == hero_id,
                                                       Hero.league == league_id,
                                                       Hero.is_battlecup.is_(is_battlecup))).first()[0]

    teamq = session.query(TeamHero).filter(TeamHero.user == user).filter(TeamHero.league == league_id).\
                                                filter(TeamHero.is_battlecup.is_(is_battlecup))
    teamq_hero = teamq.filter(TeamHero.hero_id == hero_id)

    # not ideal that these arent parallelelly implemented
    if is_battlecup:
        user_money = 50.0 - sum([hero.value for hero in
                                 session.query(Hero).filter(and_(Hero.is_battlecup.is_(is_battlecup),
                                                                 Hero.league == league_id,
                                                                 Hero.id.in_([x.hero_id for x in teamq.all()])))
                                 ])
    else:
        user_money_q = session.query(LeagueUser.money).filter(and_(LeagueUser.username == user,
                                                               LeagueUser.league == league_id))
        user_money = user_money_q.first()[0]
    if user_money < hero_value:
        return {"success": False, "message": "ERROR: Insufficient credits"}

    new_credits = round(user_money - hero_value, 1)

    if teamq.count() >= 5:
        return {"success": False, "message": "ERROR: Team is currently full"}
    if teamq_hero.first():
        print teamq_hero.all()
        print is_battlecup, "is btttccpo"
        return {"success": False, "message": "ERROR: Hero already in team"}
    else:
        session.add(TeamHero(user, hero_id, league=league_id, is_battlecup=is_battlecup))
        if not is_battlecup:
            user_money_q.update({LeagueUser.money: new_credits})
    return {"success": True, "message": "Hero successfully bought", "action": "buy", "hero": hero_id,
            "new_credits": new_credits}