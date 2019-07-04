from fantasydota.lib.constants import DEFAULT_LEAGUE
from fantasydota.lib.general import all_view_wrapper
from fantasydota.models import (
    DBSession,
    Friend, User)
from pyramid.httpexceptions import (
    HTTPForbidden)
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
    return all_view_wrapper({}, session, user_id)


@view_config(route_name='view_privacy', renderer='../templates/privacy.mako')
def view_privacy(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    return all_view_wrapper({}, session, user_id)


@view_config(route_name='view_rules', renderer='../templates/rules.mako')
def view_rules(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    return all_view_wrapper(
        {}, session, user_id
    )


@view_config(route_name="hall_of_fame", renderer="../templates/hall_of_fame.mako")
def hall_of_fame(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    return all_view_wrapper(
        {}, session, user_id
    )


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


@view_config(route_name='index', renderer='../templates/index.mako')
def index(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    return all_view_wrapper(
        {}, session, user_id
    )


@view_config(route_name='collection', renderer='../templates/collection.mako')
def collection(request):
    session = DBSession()
    league_id = int(request.params.get('league', DEFAULT_LEAGUE))
    user_id = authenticated_userid(request)
    return_dict = {'league_id': league_id}
    return all_view_wrapper(return_dict, session, user_id)
