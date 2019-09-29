from local_settings import FANTASY_API_KEY

import json
import re
import urllib2
from pyramid.response import Response

from fantasydota.auth import get_user
from fantasydota.lib.constants import API_URL
from fantasydota.lib.general import all_view_wrapper, get_league_id
from fantasydota.models import (
    DBSession,
    Friend, User, League, Team)
from pyramid.httpexceptions import (
    HTTPForbidden, HTTPFound, HTTPNotFound)
from pyramid.security import (
    authenticated_userid)
from pyramid.view import (
    view_config,
)
from sqlalchemy import and_


@view_config(route_name='view_faq', renderer='../templates/faq.mako')
def view_faq(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    return all_view_wrapper(request, {}, session, user_id)


@view_config(route_name='view_privacy', renderer='../templates/privacy.mako')
def view_privacy(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    return all_view_wrapper(request, {}, session, user_id)


@view_config(route_name='view_rules', renderer='../templates/rules.mako')
def view_rules(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    return all_view_wrapper(
        request, {}, session, user_id
    )


@view_config(route_name="hall_of_fame", renderer="../templates/hall_of_fame.mako")
def hall_of_fame(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    return all_view_wrapper(
        request, {}, session, user_id
    )


@view_config(route_name="add_friend", renderer="json")
def add_friend(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if user_id is None:
        raise HTTPForbidden()

    new_friend = request.POST["newFriend"].lower()
    new_friend_id = session.query(User.id).filter(User.username == new_friend).first()
    if not new_friend_id:
        return {"success": False, "message": "Sorry. That person does not exist"}
    elif session.query(Friend).filter(and_(Friend.user_id == user_id, Friend.friend == new_friend_id[0])).first():
        return {"success": False, "message": "You have already added that friend"}
    else:
        session.add(Friend(user_id, new_friend_id[0]))
        return {"success": True, "message": "Friend successfully added"}


@view_config(route_name='index', renderer='../templates/index.mako')
def index(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    return all_view_wrapper(
        request, {}, session, user_id
    )


@view_config(route_name='collection', renderer='../templates/collection.mako')
def collection(request):
    session = DBSession()
    league_id = get_league_id(request)
    user_id = authenticated_userid(request)
    return_dict = {'league_id': league_id}
    return all_view_wrapper(request, return_dict, session, user_id)


@view_config(route_name='change_league', renderer='../templates/collection.mako')
def change_league(request):
    league_id = get_league_id(request)
    response = HTTPFound(location=re.sub("[?&]league_id=\d+", "", request.environ.get('HTTP_REFERER', '/team')))
    response.set_cookie('league_id', value=str(league_id), max_age=31536000)  # one year
    return response


@view_config(route_name='join_league')
def join_league(request):
    session = DBSession()
    league_id = get_league_id(request)
    invite_link = request.matchdict['invite_link']
    if session.query(League).filter(and_(League.id == league_id, League.invite_link == invite_link)).first():
        try:
            user_id = authenticated_userid(request)
            user = session.query(User).filter(User.id == user_id).first()
            url = "{}users/{}/join/{}?username={}".format(API_URL, user_id, league_id, user.username)
            req = urllib2.Request(
                url, data=json.dumps({"username": user.username, "userId": user.id}), headers={
                    # TODO replace with chief apikey
                    'apiKey': FANTASY_API_KEY,
                    'User-Agent': 'fantasy-dota-backend',
                    "Content-Type": "application/json"
                }
            )
            response = urllib2.urlopen(req)
            print(response.read())
            session.add(Team(user.id, league_id, user.username))
        except urllib2.HTTPError as e:
            text = e.read()
            return Response(text, status=e.code, content_type="application/json")

        return HTTPFound('/draft')
    else:
        return HTTPNotFound('Not found league or invite link')
