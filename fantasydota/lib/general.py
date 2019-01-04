from fantasydota.lib.constants import DEFAULT_LEAGUE, API_URL
from fantasydota.models import Notification
from pyramid.security import authenticated_userid
from sqlalchemy import desc


def add_notifications(return_dict, session, user_id):
    notifications = session.query(Notification).filter(Notification.user == user_id)\
        .filter(Notification.seen.is_(False)).order_by(desc(Notification.id)).limit(10).all()
    return_dict['notifications'] = notifications
    return return_dict


def all_view_wrapper(return_dict, session, request):
    user_id = authenticated_userid(request)
    if user_id:
        return_dict = add_notifications(return_dict, session, user_id)
    else:
        return_dict['notifications'] = []
    return_dict['api_base_url'] = API_URL
    return_dict['league_id'] = return_dict.get('league_id', DEFAULT_LEAGUE)
    return return_dict
