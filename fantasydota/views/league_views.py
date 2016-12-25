import datetime
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import and_
from sqlalchemy import or_

from fantasydota import DBSession
from fantasydota.models import User, TeamHeroLeague, HeroLeague, League, UserLeague


@view_config(route_name='view_league', renderer='templates/view_account.mako')
def view_league(request):
    session = DBSession()
    user = authenticated_userid(request)
    if user is None:
        return HTTPFound('/login')
    message_type = request.params.get('message_type')
    message = request.params.get('message')
    league_id = request.params.get('league')

    userq = session.query(UserLeague).filter(User.username == user).first()
    transfer_open = session.query(League).filter(League.id == league_id).first().transfer_open

    print "user:", user
    team_ids = session.query(TeamHeroLeague.hero, TeamHeroLeague.active, TeamHeroLeague.to_trade).\
        filter(and_(TeamHeroLeague.user == user, TeamHeroLeague.league == league_id)).all()
    team = [{'hero_': session.query(HeroLeague).filter(and_(HeroLeague.hero == my_hero[0],
                                                            TeamHeroLeague.league == league_id)).first(),
             'active': my_hero[1],
             'to_trade': my_hero[2]}
            for my_hero in team_ids]

    heroes = session.query(HeroLeague).filter(TeamHeroLeague.league == league_id).all()
    #transfer_open = True if request.registry.settings["transfers"] else False
    return {'user': userq, 'team': team, 'heroes': heroes, 'message': message,
            'message_type': message_type, 'transfer_open': transfer_open}


@view_config(route_name="sell_hero_league", renderer="json")
def sell_hero_league(request):
    session = DBSession()
    user = authenticated_userid(request)
    if user is None:
        raise HTTPForbidden()

    hero_id = request.POST["hero"]
    transfer_think_open = request.POST["transfer"]
    league_id = request.POST["league_id"]
    transfer_actually_open = session.query(League.transfer_open).filter(League.id == league_id).first()[0]
    if transfer_think_open == "true" and not transfer_actually_open or \
                            transfer_think_open == "false" and transfer_actually_open:
        return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    hero_value = session.query(HeroLeague.value).filter(and_(HeroLeague.hero == hero_id,
                                                             HeroLeague.league == league_id)).first()[0]
    user_money = session.query(UserLeague.money).filter(and_(UserLeague.username == user,
                                                             HeroLeague.league == league_id)).first()
    new_credits = round(user_money[0] + hero_value, 1)

    thero_q = session.query(TeamHeroLeague).filter(and_(TeamHeroLeague.user == user,
                                                        HeroLeague.league == league_id)).filter(TeamHeroLeague.hero == hero_id)
    if transfer_actually_open or not thero_q.first().active:
        check_hero = session.query(TeamHeroLeague).filter(and_(TeamHeroLeague.user == user,
                                                               TeamHeroLeague.hero == hero_id,
                                                               TeamHeroLeague.league == league_id,
                                                               )
                                                          )
        if check_hero.first():
            check_hero.delete()
            user_money = new_credits
            # do I need to commit?
        else:
            return verifyHeroCount({"success": False, "message": "ERROR: Hero is not in your team to sell"})
    else:
        thero_q.update({TeamHeroLeague.to_trade: True})
        user_money = new_credits

    return {"success": True, "message": "Hero successfully sold", "action": "sell", "hero": hero_id,
            "new_credits": new_credits}


@view_config(route_name="buy_hero_league", renderer="json")
def buy_hero_league(request):
    session = DBSession()
    user = authenticated_userid(request)
    if user is None:
        raise HTTPForbidden()

    hero_id = request.POST["hero"]
    league_id = request.POST["league_id"]
    transfer_think_open = request.POST["transfer"]
    transfer_actually_open = session.query(League.transfer_open).filter(League.id == league_id).first()[0]
    if transfer_think_open == "true" and not transfer_actually_open or \
        transfer_think_open == "false" and transfer_actually_open:
            return {"success": False, "message": "Transfer window just open/closed. Please reload page"}
    hero_value = session.query(HeroLeague.value).filter(HeroLeague.hero_id == hero_id).first()[0]
    user_money = float(session.query(User.money).filter(User.username == user).first()[0])
    if user_money < hero_value:
        return {"success": False, "message": "ERROR: Insufficient credits"}

    teamq = session.query(TeamHeroLeague).filter(and_(TeamHeroLeague.user == user,
                                                      HeroLeague.league == league_id)).filter(TeamHeroLeague.league == league_id)
    a = teamq.filter(or_(and_(TeamHeroLeague.to_trade == True, TeamHeroLeague.active == False),
                            and_(TeamHeroLeague.active == True, TeamHeroLeague.to_trade == False))).\
            count()
    teamq2 = teamq.filter(and_(TeamHeroLeague.hero == hero_id, TeamHeroLeague.to_trade == True, TeamHeroLeague.active == True))
    teamq3 = teamq.filter(and_(TeamHeroLeague.hero == hero_id, TeamHeroLeague.to_trade == True, TeamHeroLeague.active == False))

    new_credits = round(user_money - hero_value, 1)
    if a >= 5:
        return {"success": False, "message": "ERROR: Team is currently full"}
    if teamq2.first():
        teamq2.update({TeamHeroLeague.to_trade: False})
        session.query(User).filter(User.username == user). \
            update({User.money: new_credits})
    elif teamq.filter(and_(TeamHeroLeague.hero == hero_id, TeamHeroLeague.to_trade != True)).first() or teamq3.first():
        return {"success": False, "message": "ERROR: Hero already in team"}
    elif transfer_actually_open:
        session.add(TeamHeroLeague(user, hero_id, active=True, to_trade=False, league=league_id))
        session.query(User).filter(User.username == user).filter(TeamHeroLeague.league == league_id).\
            update({User.money: new_credits})
    else:
        session.add(TeamHeroLeague(user, hero_id, active=False, to_trade=True, league=league_id))
        session.query(UserLeague).filter(User.username == user).filter(TeamHeroLeague.league == league_id). \
            update({User.money: new_credits})
    return {"success": True, "message": "Hero successfully bought", "action": "buy", "hero": hero_id,
            "new_credits": new_credits}
