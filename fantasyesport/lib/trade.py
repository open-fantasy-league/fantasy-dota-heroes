from fantasyesport.models import League, Hero, LeagueUser, TeamHero
from sqlalchemy import and_

def cost(hero_value, days, hero_id):
        if hero_id <= 3:  # team flash
            return round(hero_value * (1 - (0.1 * (days - 1))), 1)
        else:
            return round(hero_value * (1 - (0.1 * (days - 1))), 1)

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
    # add league filters
    user_money = 40.0 - sum([session.query(TeamHero.cost).filter(TeamHero.user_id == user_id).filter(TeamHero.hero_id == hero.id).filter(TeamHero.is_battlecup.is_(is_battlecup)).first()[0] for hero in
                             session.query(Hero).filter(and_(Hero.is_battlecup.is_(is_battlecup),
                                                             Hero.league == league_id,
                                                             Hero.id.in_([x[0] for x in teamq.all()])))
                             ])

    teamq_hero = session.query(TeamHero).filter(and_(TeamHero.user_id == user_id,
                                                     TeamHero.is_battlecup.is_(is_battlecup),
                                                     TeamHero.league == league_id))
    if teamq_hero.first():
        check_hero = teamq_hero.filter(TeamHero.hero_id == hero_id)
        check_hero_res = check_hero.first()

        if check_hero_res:
            new_credits = round(user_money + check_hero_res.cost, 1)
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
	
    user_money = 40.0 - sum([session.query(TeamHero.cost).filter(TeamHero.user_id == user_id).filter(TeamHero.hero_id == hero.id).filter(TeamHero.is_battlecup.is_(is_battlecup)).first()[0] for hero in
                             session.query(Hero).filter(and_(Hero.is_battlecup.is_(is_battlecup),
                                                             Hero.league == league_id,
                                                             Hero.id.in_([x.hero_id for x in teamq.all()])))
                             ])

    cost_ =   cost(hero_value, days, hero_id)# knock off 10% for every extra game round loaned for
    if user_money < cost_:
        return {"success": False, "message": "ERROR: Insufficient credits"}

    new_credits = round(user_money - cost_, 1)

    # 3 players per team
    team = [TeamHero.get_team(x.hero_id) for x in teamq.all()]
    if TeamHero.get_team(hero_id) in team:
        return {"success": False, "message": "ERROR: Already have a player from that team"}
    if teamq.count() >= 4:
        return {"success": False, "message": "ERROR: Team is currently full"}
    else:
        session.add(TeamHero(user_id, hero_id, league_id, is_battlecup, days, cost_))
    return {"success": True, "message": "Hero successfully loaned for %s days" % days,
            "action": "buy", "hero": hero_id,
            "new_credits": new_credits}
