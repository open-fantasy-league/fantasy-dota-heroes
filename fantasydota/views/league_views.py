import datetime

from fantasydota.lib.trade import buy, sell
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import and_
from sqlalchemy import or_

from fantasydota import DBSession
from fantasydota.models import User, League, LeagueUser, Hero, TeamHero, LeagueUserDay


@view_config(route_name='view_league', renderer='../templates/league.mako')
def view_league(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    message_type = request.params.get('message_type')
    message = request.params.get('message')

    league_id = int(request.params.get("league")) if request.params.get("league") else None \
        or request.registry.settings["default_league"]

    league = session.query(League).filter(League.id == league_id).first()

    class FakeUser():  # hacky quick way so unlogged in users can see the page
        username = ""
        league = league_id
        money = 40.0
        points = 0
        picks = 0
        bans = 0
        wins = 0
        points_rank = None
        wins_rank = None
        picks_rank = None
        bans_rank = None

    if user_id is None:
        message = "You must login to pick team"

        userq = FakeUser()
        team = []
        username = ""
        #return HTTPFound('/login')
    else:

        userq = session.query(LeagueUser).filter(LeagueUser.user_id == user_id).first()
        if not userq:
            username = session.query(User.username).filter(User.id == user_id).first()[0]
            user_league = LeagueUser(user_id, username, league.id)
            session.add(user_league)
            session.flush()
            for i in range(league.days):
                if i >= league.stage2_start:
                    stage = 2
                elif i >= league.stage1_start:
                    stage = 1
                else:
                    stage = 0
                session.add(LeagueUserDay(user_league.id, i, stage))

            userq = FakeUser()  # so dont have to deal with a commit mid-request

        team = session.query(Hero, TeamHero).filter(and_(
                                               Hero.is_battlecup.is_(False),
                                               Hero.league == league_id)).\
            filter(and_(TeamHero.user_id == user_id, TeamHero.league == league_id,
                        TeamHero.is_battlecup.is_(False))).\
            join(TeamHero).all()
        print team
        username = session.query(User.username).filter(User.id == user_id).first()[0]
    heroes = session.query(Hero).filter(and_(Hero.league == league_id,
                                             Hero.is_battlecup.is_(False))).all()

    #transfer_open = True if request.registry.settings["transfers"] else False
    return {'username': username, 'userq': userq, 'team': team, 'heroes': heroes, 'message': message,
            'message_type': message_type, 'league': league}


@view_config(route_name="sell_hero_league", renderer="json")
def sell_hero_league(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        return {"success": False, "message": "Please create an account to play! :)"}

    hero_id = request.POST["hero"]
    # transfer_think_open = request.POST["transfer"] really doesnt matter what the user thinks! :D
    league_id = request.POST["league"]
    transfer_actually_open = session.query(League.transfer_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    return sell(session, user_id, hero_id, league_id, False)


@view_config(route_name="buy_hero_league", renderer="json")
def buy_hero_league(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        return {"success": False, "message": "Please login to play! :)"}

    hero_id = int(request.POST["hero"])
    league_id = int(request.POST["league"])
    days = int(request.POST["days"])
    # transfer_think_open = request.POST["transfer"] really doesnt matter what the user thinks! :D
    transfer_actually_open = session.query(League.transfer_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    return buy(session, user_id, hero_id, league_id, False, days)
