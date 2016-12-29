import datetime

from fantasydota.lib.trade import buy, sell
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import and_
from sqlalchemy import or_

from fantasydota import DBSession
from fantasydota.models import User, League, LeagueUser, Hero, TeamHero


@view_config(route_name='view_league', renderer='../templates/league.mako')
def view_league(request):
    session = DBSession()
    user = authenticated_userid(request)
    if user is None:
        return HTTPFound('/login')
    message_type = request.params.get('message_type')
    message = request.params.get('message')
    league_id = int(request.params.get("league")) if request.params.get("league") else None \
        or request.registry.settings["default_league"]

    userq = session.query(LeagueUser).filter(User.username == user).first()
    league = session.query(League).filter(League.id == league_id).first()

    print "user:", user
    team_ids = [res[0]for res in session.query(TeamHero.hero_id).\
        filter(and_(TeamHero.user == user, TeamHero.league == league_id,
                    TeamHero.is_battlecup.is_(False))).all()]
    team = session.query(Hero).filter(and_(Hero.id.in_(team_ids),
                                           Hero.is_battlecup.is_(False),
                                           Hero.league == league_id)).all()
    heroes = session.query(Hero).filter(and_(Hero.league == league_id,
                                             Hero.is_battlecup.is_(False))).all()

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

    return sell(session, user, hero_id, league_id, False)


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

    return buy(session, user, hero_id, league_id, False)
