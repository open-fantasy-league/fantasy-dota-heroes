from pyramid.security import authenticated_userid
from pyramid.view import view_config
from sqlalchemy import and_

from fantasydota import DBSession
from fantasydota.lib.trade import buy, sell, swap_in, swap_out
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
        money = 50.0
        reserve_money = 50.0
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
        reserve_team = []
        #return HTTPFound('/login')
    else:

        userq = session.query(LeagueUser).filter(and_(
            LeagueUser.league == league.id, LeagueUser.user_id == user_id
        )).first()
        if not userq:
            username = session.query(User.username).filter(User.id == user_id).first()[0]
            user_league = LeagueUser(user_id, username, league.id)
            session.add(user_league)
            for i in range(league.days):
                if i >= league.stage2_start:
                    stage = 2
                elif i >= league.stage1_start:
                    stage = 1
                else:
                    stage = 0
                session.add(LeagueUserDay(user_id, username, league.id, i, stage))

            userq = FakeUser()  # so dont have to deal with a commit mid-request

        team = session.query(Hero, TeamHero).filter(Hero.league == league_id).\
            filter(and_(TeamHero.user_id == user_id, TeamHero.league == league_id)).filter(TeamHero.reserve.is_(False)).\
            join(TeamHero).all()
        reserve_team = session.query(Hero, TeamHero).filter(Hero.league == league_id).\
            filter(and_(TeamHero.user_id == user_id, TeamHero.league == league_id)).filter(TeamHero.reserve.is_(True)).\
            join(TeamHero).all()
        username = session.query(User.username).filter(User.id == user_id).first()[0]
    heroes = session.query(Hero).filter(Hero.league == league_id).all()

    #transfer_open = True if request.registry.settings["transfers"] else False
    return {'username': username, 'userq': userq, 'team': team, 'heroes': heroes, 'message': message,
            'message_type': message_type, 'league': league, 'reserve_team': reserve_team}


@view_config(route_name="sell_hero", renderer="json")
def sell_hero(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        return {"success": False, "message": "Please create an account to play! :)"}

    hero_id = request.POST["hero"]
    # transfer_think_open = request.POST["transfer"] really doesnt matter what the user thinks! :D
    league_id = request.POST["league"]
    reserve = bool(int(request.POST["reserve"]))
    transfer_actually_open = session.query(League.transfer_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    return sell(session, user_id, hero_id, league_id, reserve)


@view_config(route_name="buy_hero", renderer="json")
def buy_hero(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        return {"success": False, "message": "Please login to play! :)"}

    hero_id = int(request.POST["hero"])
    league_id = int(request.POST["league"])
    reserve = bool(int(request.POST["reserve"]))
    # transfer_think_open = request.POST["transfer"] really doesnt matter what the user thinks! :D
    transfer_actually_open = session.query(League.transfer_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    return buy(session, user_id, hero_id, league_id, reserve)


@view_config(route_name="swap_in_hero", renderer="json")
def swap_in_hero(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        return {"success": False, "message": "Please login to play! :)"}

    hero_id = int(request.POST["hero"])
    league_id = int(request.POST["league"])
    # transfer_think_open = request.POST["transfer"] really doesnt matter what the user thinks! :D
    transfer_actually_open = session.query(League.swap_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        return {"success": False, "message": "Swap window just open/closed. Please reload page"}

    return swap_in(session, user_id, hero_id, league_id)


@view_config(route_name="swap_out_hero", renderer="json")
def swap_out_hero(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        return {"success": False, "message": "Please login to play! :)"}

    hero_id = int(request.POST["hero"])
    league_id = int(request.POST["league"])
    # transfer_think_open = request.POST["transfer"] really doesnt matter what the user thinks! :D
    transfer_actually_open = session.query(League.swap_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        return {"success": False, "message": "Swap window just open/closed. Please reload page"}

    return swap_out(session, user_id, hero_id, league_id)
