import datetime

import urllib2

import json
from pyramid.response import Response

from fantasydota.lib.constants import DEFAULT_LEAGUE, API_URL, HERO_LEAGUE
from fantasydota.models import Notification, User
from pyramid.security import authenticated_userid
from sqlalchemy import desc


def add_notifications(return_dict, session, user_id):
    notifications = session.query(Notification).filter(Notification.user == user_id)\
        .filter(Notification.seen.is_(False)).order_by(desc(Notification.id)).limit(10).all()
    return_dict['notifications'] = notifications
    return return_dict


def get_league_id(request):
    return int(request.params.get('league_id', request.cookies.get('league_id', DEFAULT_LEAGUE)))


def all_view_wrapper(request, return_dict, session, user_id=None, user=None):
    return_dict['user_id'] = user_id
    user = user or session.query(User).filter(User.id == user_id).first()
    return_dict['user'] = user
    if user:
        return_dict = add_notifications(return_dict, session, user_id)
        return_dict['username'] = user.username
    else:
        return_dict['notifications'] = []
        return_dict['username'] = ""
    return_dict['api_base_url'] = API_URL
    league_id = return_dict.get('league_id', get_league_id(request))
    return_dict['league_id'] = league_id
    return_dict['api_registered'] = return_dict.get('api_registered', False)
    return_dict['is_card_system'] = league_id == DEFAULT_LEAGUE
    return_dict['leagues'] = {DEFAULT_LEAGUE: 'Pros', HERO_LEAGUE: 'Heroes'}
    return return_dict


def post_api_json(url, data, fe_api_key=None):
    print("in postapijson")
    try:
        req = urllib2.Request(url, data=json.dumps(data),
                              headers={'apiKey': fe_api_key, "Content-Type": "application/json"})
        response = urllib2.urlopen(req)
        print(response.read())
    except urllib2.HTTPError as e:
        print(e.read())


def api_request(url, data, api_key):
    try:
        req = urllib2.Request(
            url, data=json.dumps(data), headers={
                'apiKey': api_key,
                'User-Agent': 'fantasy-dota-frontend',
                "Content-Type": "application/json"
            }
        )
        response = urllib2.urlopen(req)
        return json.loads(response.read())
    except urllib2.HTTPError as e:
        text = e.read()
        return Response(text, status=e.code, content_type="application/json")
    except Exception as e:
        return Response(e.message, status=500)


def format_time(time_):
    return datetime.datetime.fromtimestamp(time_).strftime('%Y-%m-%d %H:%M:%S')
