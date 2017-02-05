import datetime

from fantasydota.models import (
    DBSession,
    Friend, User)
from fantasydota.util.random_function import add_months, bprint
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPForbidden)
from pyramid.security import (
    authenticated_userid)
from pyramid.view import (
    view_config,
)
from sqlalchemy import and_


@view_config(route_name='view_faq', renderer='../templates/faq.mako')
def view_faq(request):
    return {}


@view_config(route_name='view_rules', renderer='../templates/rules.mako')
def view_rules(request):
    return {}


@view_config(route_name='view_index')
def view_index(request):
    return HTTPFound("/viewLeague")


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


@view_config(route_name="switch_transfers", renderer="string")
def switch_transfers(request):
    change = request.params.get("state")
    if request.remote_addr not in ('127.0.0.1', '149.210.217.128'):
        raise HTTPForbidden()
    bprint(request.remote_addr)
    if change == 'open':
        request.registry.settings.update({"transfers": True})
        return "transfer window opened"
    elif change == 'closed':
        request.registry.settings.update({"transfers": False})
        return "transfer window closed"
    else:
        return "incorrect state param"


@view_config(route_name="news", renderer="../templates/news.mako")
def news(request):
    return {}


@view_config(route_name="hall_of_fame", renderer="../templates/hall_of_fame.mako")
def hall_of_fame(request):
    return {}


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
