import datetime
import json

import ast

from fantasydota.auth import get_user
from fantasydota.scripts.end_of_day import end_of_day
from fantasydota.scripts.start_of_day import start_of_day
from pyramid.response import Response

from fantasydota.lib.general import add_other_games
from fantasydota.lib.herolist import heroes
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPForbidden)
from pyramid.security import (
    authenticated_userid, remember)
from pyramid.view import (
    view_config,
)
from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import func

from fantasydota.lib.items import ITEMS
from fantasydota.models import (
    DBSession,
    Friend, User, GuessUser, HeroGame, ItemBuild)
from fantasydota.util.random_function import add_months, bprint


@view_config(route_name='view_faq', renderer='../templates/faq.mako')
def view_faq(request):
    session = DBSession()
    return add_other_games(session, request.game, {})


@view_config(route_name='view_rules', renderer='../templates/rules.mako')
def view_rules(request):
    session = DBSession()
    return add_other_games(session, request.game, {'game_code': request.game})


@view_config(route_name='change_game')
def change_game(request):
    # https://userlinux.net/pyramid-set-cookie-returning-httpfound.html
    response = HTTPFound(location=request.environ['HTTP_REFERER'])
    response.set_cookie('game', value=request.params.get('game', 'DOTA'), max_age=315360000)
    return response


@view_config(route_name='start_day_req', renderer='string')
def start_day_req(request):
    start_of_day(league_id=5627)
    return "Started day"


@view_config(route_name='end_day_req', renderer='string')
def end_day_req(request):
    end_of_day(league_id=5627)
    return "Ended day"


@view_config(route_name="add_friend", renderer="json")
def add_friend(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        raise HTTPForbidden()

    new_friend = request.POST["newFriend"].lower()
    new_friend_id = session.query(User.id).filter(User.username == new_friend).first()
    if session.query(Friend).filter(and_(Friend.user_id == user_id, Friend.friend == new_friend)).first():
        return {"success": False, "message": "You have already added that friend"}
    elif not new_friend_id:
        return {"success": False, "message": "Sorry. That person does not exist"}
    else:
        session.add(Friend(user_id, new_friend_id[0]))
        return {"success": True, "message": "Friend successfully added"}


@view_config(route_name="news", renderer="../templates/news.mako")
def news(request):
    return {}


@view_config(route_name="hall_of_fame", renderer="../templates/hall_of_fame.mako")
def hall_of_fame(request):
    session = DBSession()
    return add_other_games(session, request.game, {'game_code': request.game})


@view_config(route_name='index', renderer='../templates/index.mako')
def index(request):
    session = DBSession()
    return_dict = {}
    return add_other_games(session, request.game, return_dict)


def get_time_range(time_range):
    if time_range == 'week':
        date_start = datetime.datetime.now() - datetime.timedelta(days=7)
        date_end = datetime.datetime.now()
    elif time_range == 'month':
        date_start = add_months(datetime.datetime.now(), -1)
        date_end = datetime.datetime.now()
    else:
        date_start = datetime.datetime(2015, 11, 1)
        date_end = datetime.datetime.now()
    return date_start, date_end
