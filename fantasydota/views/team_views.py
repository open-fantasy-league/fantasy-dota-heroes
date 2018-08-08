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
from fantasydota.lib.general import all_view_wrapper, get_league
from fantasydota.lib.trade import buy, sell, get_swap_timestamp
from fantasydota.models import User, League, LeagueUser, Hero, TeamHero, LeagueUserDay, Game
from sqlalchemy import desc


@view_config(route_name='view_team_optional', renderer='../templates/team.mako')
@view_config(route_name='view_team', renderer='../templates/team.mako')
def view_team(request):
    session = DBSession()
    # request.matchdict.get('game')
    user_id = authenticated_userid(request)
    league_id = int(request.params.get('league', get_league(request, session)))
    league = session.query(League).filter(League.id == league_id).first()
    game = session.query(Game).filter(Game.id == league.game).first()
    message_type = request.params.get('message_type')
    message = request.params.get('message')

    # league_id = int(request.params.get("league") or
    #                 (in_progress_league(session, game.id) or next_league(session, game.id)).id)

    class FakeUser():  # hacky quick way so unlogged in users can see the page

        def __init__(self, league):
            self.username = ""
            self.league = league_id
            self.money = 10 * game.team_size
            self.points = 0
            self.picks = 0
            self.bans = 0
            self.wins = 0
            self.points_rank = None
            self.wins_rank = None
            self.picks_rank = None
            self.bans_rank = None
            self.swap_tstamp = None
            self.remaining_transfers = 10
            self.voided_transfers = False

    # dont blame me for the string check.
    # seems something weird coming out of the python pyramid auth system
    if user_id is None or user_id == 'None':
        message = "You must login to pick team"

        userq = FakeUser(league)
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
            user_league = LeagueUser(user_id, username, league.id, False, money=10*game.team_size, reserve_money=10*game.reserve_size)
            session.add(user_league)
            for i in range(league.days):
                if i >= league.stage2_start:
                    stage = 2
                elif i >= league.stage1_start:
                    stage = 1
                else:
                    stage = 0
                session.add(LeagueUserDay(user_id, username, league.id, i, stage))

            userq = FakeUser(league)  # so dont have to deal with a commit mid-request

        team = session.query(Hero, TeamHero).filter(Hero.league == league_id).\
            filter(and_(TeamHero.user_id == user_id, TeamHero.league == league_id)).join(TeamHero).order_by(TeamHero.reserve)\
            .order_by(desc(TeamHero.active)).all()
    heroes = session.query(Hero).filter(Hero.league == league_id).all()

    return_dict = {'username': userq.username, 'userq': userq, 'team': team, 'heroes': heroes, 'message': message,
                    'message_type': message_type, 'league': league,
                   'game': game}

    if userq.swap_tstamp:
        seconds_until_swap = userq.swap_tstamp - time.time()
        minutes = seconds_until_swap // 60
        return_dict['time_until_swap'] = divmod(minutes, 60)
    return_dict = all_view_wrapper(return_dict, session, request, league_id=league_id)
    result = render('fantasydota:templates/team.mako',
                    return_dict,
                    request=request)
    response = Response(result)
    response.set_cookie('league', value=str(league_id), max_age=315360000)
    return response


@view_config(route_name="sell_hero", renderer="json")
def sell_hero(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        return {"success": False, "message": "Please create an account to play! :)"}

    hero_id = request.POST["hero"]
    league_id = request.POST["league"]
    l_user = session.query(LeagueUser).filter(LeagueUser.league == league_id).filter(
        LeagueUser.user_id == user_id).first()
    league = session.query(League).filter(League.id == league_id).first()
    started = league.status > 0
    if l_user.swap_tstamp:
        return {"success": False,
                "message": "You have already made transfers within the last hour"
                           " You cannot make more until this hour period has passed"}

    if l_user.voided_transfers:
        l_user.voided_transfers = False
        return {"success": False, "message": "Hero value recalibration just occurred. "
                                             "Therefore your pending transfers have been reset. Apologies.",
                "reload": True}

    return sell(session, l_user, hero_id, league_id, started=started)


@view_config(route_name="buy_hero", renderer="json")
def buy_hero(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        return {"success": False, "message": "Please login to play! :)"}

    hero_id = int(request.POST["hero"])
    league_id = int(request.POST["league"])
    l_user = session.query(LeagueUser).filter(LeagueUser.league == league_id).filter(
        LeagueUser.user_id == user_id).first()
    league = session.query(League).filter(League.id == league_id).first()
    started = league.status > 0
    # if not transfer_actually_open:
    #     else:
    #         return {"success": False, "message": "Transfer window just open/closed. Please reload page"}
    if l_user.swap_tstamp:
        return {"success": False,
                "message": "You already have pending transfers."
                           " You must wait the hour transfer cooldown"}

    if l_user.voided_transfers:
        l_user.voided_transfers = False
        return {"success": False, "message": "Hero value recalibration just occurred. "
                                             "Therefore your pending transfers have been reset. Apologies.",
                "reload": True}

    return buy(session, l_user, hero_id, league_id, started=started)


@view_config(route_name="confirm_transfer", renderer="json")
def confirm_transfer(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        return {"success": False, "message": "Please login to play! :)"}

    league_id = int(request.params.get("league"))
    l_user = session.query(LeagueUser).filter(LeagueUser.league == league_id).filter(
        LeagueUser.user_id == user_id).first()
    sold_heroes = session.query(TeamHero).filter(and_(TeamHero.user_id == user_id,
                                                     TeamHero.league == league_id)).filter(TeamHero.reserve.is_(True)).count()
    if l_user.voided_transfers:
        l_user.voided_transfers = False
        return {"success": False, "message": "Hero value recalibration occurred before confirm transfers went through. "
                                             "Therefore your pending transfers have been reset. Apologies.",
                "reload": True}
    if sold_heroes > l_user.remaining_transfers:
        return {"success": False, "message": "You have insufficient remaining transfers to perform this change"}
    else:
        l_user.remaining_transfers -= sold_heroes
    l_user.swap_tstamp = get_swap_timestamp()
    return {"success": True, "message": "Successfully confirmed transfers"}

