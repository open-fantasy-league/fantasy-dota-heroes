import datetime
import json

import ast

from fantasydota.lib.herolist import heroes
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPForbidden)
from pyramid.security import (
    authenticated_userid)
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
    return {}


@view_config(route_name='view_rules', renderer='../templates/rules.mako')
def view_rules(request):
    return {}


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
    return {}


@view_config(route_name="guess_the_hero", renderer="../templates/guesshero.mako")
def guess_the_hero(request):
    session = DBSession()
    ip = request.remote_addr
    user_agent = request.user_agent

    identifier = str(ip) + user_agent
    user = session.query(GuessUser).filter(GuessUser.identifier_hash == identifier).first()
    message = request.params.get("message", "")
    match_id = request.params.get("match_id", "")
    correct_hero = request.params.get("correct_hero", "")
    success = ast.literal_eval(request.params.get("success", True))

    if not user:
        hero_game_id = session.query(HeroGame.id).order_by(func.random()).first()[0]
        user = GuessUser(identifier, hero_game_id)
        session.add(user)
    else:
        hero_game_id = user.current_hero_game

    # 0 is empty item slot
    items = session.query(ItemBuild).filter(ItemBuild.hero_game == hero_game_id). \
        filter(ItemBuild.item != 0).order_by(ItemBuild.slot).all()
    players = session.query(GuessUser).order_by(desc(GuessUser.max_streak)).limit(10).all()

    heroes_ = heroes
    item_names = []
    for item in items:
        item_names.append([i["name"].replace("ward_dispenser", "ward_observer")
                           for i in ITEMS if i["id"] == item.item][0])
        # TODO add the mixed wards image and remove replace
    # TODO people can keep reloading the page
    # server-side timing mens they cant cheat this way
    # does make javascript timer innaccurate though

    #hero_id = session.query(HeroGame.hero_id).filter(HeroGame.id == hero_game_id).first()[0]
    #cheat = [hero["name"] for hero in heroes if hero["id"] == hero_id][0]
    return {"items": item_names, "players": players, "user": user, "heroes": heroes_, "message": message,
            "match_id": match_id, "correct_hero": correct_hero, "success": success}


@view_config(route_name="do_guess", renderer="../templates/guesshero.mako")
def do_guess(request):
    session = DBSession()
    ip = request.remote_addr
    user_agent = request.user_agent

    identifier = str(ip) + user_agent
    user = session.query(GuessUser).filter(GuessUser.identifier_hash == identifier).first()
    if not user:
        message = "Whoops. Something went very wrong with site. Sorry :("
        return HTTPFound(location=request.route_url('guess_the_hero', _query={"message": message
                                                                              }))
    username = request.params.get("username")

    if user.username != username:
        # Prevent page injections
        user.username = ''.join([i for i in username if i.isalpha()])

    now = datetime.datetime.now()
    guess = request.params.get("guess")
    # care. we still need to check if there are other separate matches
    correct_answer = session.query(HeroGame).filter(HeroGame.id == user.current_hero_game).first()
    correct_hero = [hero["name"] for hero in heroes if hero["id"] == correct_answer.hero_id][0]
    success = False
    if user.guess_in_time(now):
        if user.match_guess(session, guess):
            user.streak += 1
            user.max_streak = max(user.streak, user.max_streak)
            message = "Correct!"
            success = True
        else:
            message = "Incorrect guess!"
            user.streak = 0
    else:
        message = "Ran out of time!"
        user.streak = 0

    new_game = session.query(HeroGame).order_by(func.random()).first()
    user.current_hero_game = new_game.id
    user.last_roll = datetime.datetime.now()
    return HTTPFound(location=request.route_url('guess_the_hero', _query={"message": message,
                                                                          "match_id": correct_answer.match_id,
                                                                          "correct_hero": correct_hero,
                                                                          "success": success
                                                                          }))




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
