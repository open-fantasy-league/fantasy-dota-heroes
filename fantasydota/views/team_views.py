import time
from fantasydota.lib.league import in_progress_league, next_league
from fantasydota.lib.team import main_team_to_active
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.security import authenticated_userid, forget
from pyramid.view import view_config
from sqlalchemy import and_

from fantasydota import DBSession
from fantasydota.lib.general import all_view_wrapper
from fantasydota.lib.trade import buy, sell, swap_in, swap_out, get_swap_timestamp
from fantasydota.models import User, League, LeagueUser, Hero, TeamHero, LeagueUserDay, Game
from sqlalchemy import desc


@view_config(route_name='view_team', renderer='../templates/team.mako')
def view_team(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    league_id = int(request.params.get('league', request.league))
    league = session.query(League).filter(League.id == league_id).first()
    game = session.query(Game).filter(Game.code == league.game).first()
    if game.code == 'DOTA':
        message_type = request.params.get('message_type')
        message = request.params.get('message')

        # league_id = int(request.params.get("league") or
        #                 (in_progress_league(session, game.id) or next_league(session, game.id)).id)

        class FakeUser():  # hacky quick way so unlogged in users can see the page
            username = ""
            league = league_id
            money = 10 * game.team_size
            reserve_money = 10 * game.reserve_size
            points = 0
            picks = 0
            bans = 0
            wins = 0
            points_rank = None
            wins_rank = None
            picks_rank = None
            bans_rank = None

        # dont blame me for the string check.
        # seems something weird coming out of the python pyramid auth system
        if user_id is None or user_id == 'None':
            message = "You must login to pick team"

            userq = FakeUser()
            team = []
            username = ""
            reserve_team = []
        else:

            userq = session.query(LeagueUser).filter(and_(
                LeagueUser.league == league.id, LeagueUser.user_id == user_id
            )).first()
            if not userq:
                try:
                    username = session.query(User.username).filter(User.id == user_id).first()[0]
                except TypeError:
                    headers = forget(request)
                    print('userid: %s' % user_id)
                    print('query %s' % session.query(User.username).filter(User.id == user_id).first())
                    import traceback
                    traceback.print_exc()
                    return HTTPFound(location='/login', headers=headers)
                late_start = (league.status == 1)
                user_league = LeagueUser(user_id, username, league.id, late_start, money=10*game.team_size, reserve_money=10*game.reserve_size)
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
                join(TeamHero).order_by(TeamHero.active).all()
            reserve_team = session.query(Hero, TeamHero).filter(Hero.league == league_id).\
                filter(and_(TeamHero.user_id == user_id, TeamHero.league == league_id)).filter(TeamHero.reserve.is_(True)).\
                join(TeamHero).order_by(TeamHero.active).all()
            username = session.query(User.username).filter(User.id == user_id).first()[0]
        heroes = session.query(Hero).filter(Hero.league == league_id).all()

        return_dict = {'username': username, 'userq': userq, 'team': team, 'heroes': heroes, 'message': message,
                        'message_type': message_type, 'league': league, 'reserve_team': reserve_team,
                       'game': game}
    elif game.code == 'PUBG':
        message_type = request.params.get('message_type')
        message = request.params.get('message')

        league_id = int(request.params.get("league") or
                        (in_progress_league(session, game.id) or next_league(session, game.id)).id)

        class FakeUser():  # hacky quick way so unlogged in users can see the page
            username = ""
            league = league_id
            money = 50.0 if game == 'dota' else 40.0
            reserve_money = 50.0 if game == 'dota' else 20.0
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
        else:
            userq = session.query(LeagueUser).filter(and_(
                LeagueUser.league == league.id, LeagueUser.user_id == user_id
            )).first()
            if not userq:
                try:
                    username = session.query(User.username).filter(User.id == user_id).first()[0]
                except TypeError:
                    headers = forget(request)
                    return HTTPFound(location='/login', headers=headers)
                late_start = (league.status == 1)
                user_league = LeagueUser(user_id, username, league.id, late_start, money=game.team_size * 10.0,
                                         reserve_money=game.reserve_size * 10.0)
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

            team = session.query(Hero, TeamHero).filter(Hero.league == league_id). \
                filter(and_(TeamHero.user_id == user_id, TeamHero.league == league_id)).filter(
                TeamHero.reserve.is_(False)). \
                join(TeamHero).all()
            reserve_team = session.query(Hero, TeamHero).filter(Hero.league == league_id). \
                filter(and_(TeamHero.user_id == user_id, TeamHero.league == league_id)).filter(
                TeamHero.reserve.is_(True)). \
                join(TeamHero).all()
            username = session.query(User.username).filter(User.id == user_id).first()[0]
        heroes = session.query(Hero).filter(Hero.league == league_id).all()

        return_dict = {
            'username': username, 'userq': userq, 'team': team, 'heroes': heroes, 'message': message,
            'message_type': message_type, 'league': league, 'reserve_team': reserve_team, 'game': game,
        }
    else:
        return_dict = {'game': 'whoops'}

    transfer_open = league.transfer_open or userq.late_start == 1
    return_dict['transfer_open'] = transfer_open

    if userq.swap_tstamp:
        seconds_until_swap = userq.swap_tstamp - time.time()
        minutes = seconds_until_swap // 60
        return_dict['time_until_swap'] = divmod(minutes, 60)
    return_dict = all_view_wrapper(return_dict, session, request)
    result = render('fantasydota:templates/team.mako',
                    return_dict,
                    request=request)
    response = Response(result)
    response.set_cookie('game', value=game.code, max_age=315360000)
    return response


@view_config(route_name="sell_hero", renderer="json")
def sell_hero(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        return {"success": False, "message": "Please create an account to play! :)"}

    hero_id = request.POST["hero"]
    league_id = request.POST["league"]
    reserve = bool(int(request.POST["reserve"]))
    l_user = session.query(LeagueUser).filter(LeagueUser.league == league_id).filter(
        LeagueUser.user_id == user_id).first()
    transfer_actually_open = session.query(League.transfer_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        if l_user.late_start == 1:
            sell(session, l_user, hero_id, league_id, reserve)
        else:
            return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    return sell(session, l_user, hero_id, league_id, reserve)


@view_config(route_name="buy_hero", renderer="json")
def buy_hero(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        return {"success": False, "message": "Please login to play! :)"}

    hero_id = int(request.POST["hero"])
    league_id = int(request.POST["league"])
    reserve = bool(int(request.POST["reserve"]))
    l_user = session.query(LeagueUser).filter(LeagueUser.league == league_id).filter(
        LeagueUser.user_id == user_id).first()
    transfer_actually_open = session.query(League.transfer_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        if l_user.late_start == 1:
            buy(session, l_user, hero_id, league_id, reserve, late=True)
        else:
            return {"success": False, "message": "Transfer window just open/closed. Please reload page"}

    return buy(session, l_user, hero_id, league_id, reserve)


@view_config(route_name="swap_in_hero", renderer="json")
def swap_in_hero(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        return {"success": False, "message": "Please login to play! :)"}

    hero_id = int(request.POST["hero"])
    league_id = int(request.POST["league"])
    transfer_actually_open = session.query(League.swap_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        return {"success": False, "message": "Swap window just open/closed. If your team was incomplete it has been reset to yesterday's starting lineup"}

    return swap_in(session, user_id, hero_id, league_id)


@view_config(route_name="swap_out_hero", renderer="json")
def swap_out_hero(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        return {"success": False, "message": "Please login to play! :)"}
    hero_id = int(request.POST["hero"])
    league_id = int(request.POST["league"])
    transfer_actually_open = session.query(League.swap_open).filter(League.id == league_id).first()[0]
    if not transfer_actually_open:
        return {"success": False, "message": "Swap window just open/closed. If your team was incomplete it has been reset to yesterday's starting lineup"}

    return swap_out(session, user_id, hero_id, league_id)


@view_config(route_name="confirm_swap", renderer="json")
def confirm_swap(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        return {"success": False, "message": "Please login to play! :)"}

    league_id = int(request.params.get("league"))
    l_user = session.query(LeagueUser).filter(LeagueUser.league == league_id).filter(LeagueUser.user_id == user_id).first()
    l_user.swap_tstamp = get_swap_timestamp()
    return {"success": True, "message": "Successfully confirmed swaps"}


@view_config(route_name="confirm_transfer", renderer="json")
def confirm_transfer(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        return {"success": False, "message": "Please login to play! :)"}

    league_id = int(request.params.get("league"))
    l_user = session.query(LeagueUser).filter(LeagueUser.league == league_id).filter(LeagueUser.user_id == user_id).first()
    l_user.late_start = 2
    l_user.late_start_tstamp = time.time()
    main_team_to_active(session, l_user)
    return {"success": True, "message": "Successfully confirmed transfers"}
