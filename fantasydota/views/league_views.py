import datetime
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import and_
from sqlalchemy import or_

from fantasydota import DBSession
from fantasydota.models import User, TeamHeroLeague, HeroLeague, League, UserLeague, Hero


@view_config(route_name='view_league', renderer='../templates/view_league.mako')
def view_league(request):
    session = DBSession()
    user = authenticated_userid(request)
    if user is None:
        return HTTPFound('/login')
    message_type = request.params.get('message_type')
    message = request.params.get('message')
    league_id = int(request.params.get('league'))

    userq = session.query(UserLeague).filter(User.username == user).first()
    league = session.query(League).filter(League.id == league_id).first()

    print "user:", user
    team = session.query(TeamHeroLeague).\
        filter(and_(TeamHeroLeague.user == user, TeamHeroLeague.league == league_id)).all()
    team_ids = [res[0]for res in session.query(TeamHeroLeague.hero_id).\
        filter(and_(TeamHeroLeague.user == user, TeamHeroLeague.league == league_id)).all()]
    team = session.query(HeroLeague).filter(and_(HeroLeague.hero_id.in_(team_ids),
                                                 HeroLeague.league == league_id)).all()
    heroes = session.query(HeroLeague).filter(HeroLeague.league == league_id).all()

    #transfer_open = True if request.registry.settings["transfers"] else False
    return {'user': user, 'userq': userq, 'team': team, 'heroes': heroes, 'message': message,
            'message_type': message_type, 'league': league}


@view_config(route_name="sell_hero_league", renderer="json")
def sell_hero_league(request):
    session = DBSession()
    user = authenticated_userid(request)
    if user is None:
        raise HTTPForbidden()

    hero_id = request.POST["hero"]
    # transfer_think_open = request.POST["transfer"] really doesnt matter what the user thinks! :D
    league_id = request.POST["league"]
    transfer_actually_open = session.query(League.transfer_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    hero_value = session.query(HeroLeague.value).filter(and_(HeroLeague.hero_id == hero_id,
                                                             HeroLeague.league == league_id)).first()[0]
    user_money_q = session.query(UserLeague.money).filter(and_(UserLeague.username == user,
                                                               UserLeague.league == league_id))
    new_credits = round(user_money_q.first()[0] + hero_value, 1)

    teamq_hero = session.query(TeamHeroLeague).filter(and_(TeamHeroLeague.user == user,
                                                           TeamHeroLeague.league == league_id))
    if teamq_hero.first():
        check_hero = teamq_hero.filter(TeamHeroLeague.hero_id == hero_id)

        if check_hero.first():
            check_hero.delete()
            user_money_q.update({UserLeague.money: new_credits})
            # do I need to commit?
            return {"success": True, "message": "Hero successfully sold", "action": "sell", "hero": hero_id,
                    "new_credits": new_credits}
        else:
            return {"success": False, "message": "ERROR: Hero is not in your team to sell"}

    return {"success": False, "message": "Erm....you don't appear to be in this league. This is awkward"}


@view_config(route_name="buy_hero_league", renderer="json")
def buy_hero_league(request):
    session = DBSession()
    user = authenticated_userid(request)
    if user is None:
        raise HTTPForbidden()

    hero_id = int(request.POST["hero"])
    league_id = request.POST["league"]
    # transfer_think_open = request.POST["transfer"] really doesnt matter what the user thinks! :D
    transfer_actually_open = session.query(League.transfer_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    hero_value = session.query(HeroLeague.value).filter(HeroLeague.hero_id == hero_id).first()[0]
    user_money_q = session.query(UserLeague.money).filter(and_(UserLeague.username == user,
                                                               UserLeague.league == league_id))
    user_money = user_money_q.first()[0]
    if user_money < hero_value:
        return {"success": False, "message": "ERROR: Insufficient credits"}

    teamq = session.query(TeamHeroLeague).filter(and_(TeamHeroLeague.user == user,
                                                      TeamHeroLeague.league == league_id))
    teamq_hero = teamq.filter(TeamHeroLeague.hero_id == hero_id)

    new_credits = round(user_money - hero_value, 1)

    if teamq.count() >= 5:
        return {"success": False, "message": "ERROR: Team is currently full"}
    if teamq_hero.first():
        return {"success": False, "message": "ERROR: Hero already in team"}
    else:
        session.add(TeamHeroLeague(user, hero_id, league=league_id))
        user_money_q.update({UserLeague.money: new_credits})
    return {"success": True, "message": "Hero successfully bought", "action": "buy", "hero": hero_id,
            "new_credits": new_credits}
