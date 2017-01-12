import datetime
from pyramid.events import subscriber, BeforeRender
from social_core.backends import username
from social_core.pipeline.user import create_user, USER_FIELDS

from social_pyramid.utils import backends

from .models import DBSession, User, LeagueUserDay, LeagueUser, League


def login_user(backend, user, user_social_auth):
    backend.strategy.session_set('user_id', user.id)


def login_required(request):
    return getattr(request, 'user', None) is not None


def create_user_with_league(strategy, details, backend, user=None, *args, **kwargs):
    return_dict = create_user(strategy, details, backend, user, *args, **kwargs)
    username = kwargs.get("username", details.get("username"))
    session = DBSession()
    leagues = session.query(League).all()
    for l in leagues:
        user_league = LeagueUser(username, l.id)
        session.add(user_league)
        for i in range(l.days):
            if i >= l.stage2_start:
                stage = 2
            elif i >= l.stage1_start:
                stage = 1
            else:
                stage = 0
            session.add(LeagueUserDay(username, l.id, i, stage))

    return return_dict


def get_user(request):
    session = DBSession()
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    print "user_id: ", user_id
    print "username: ", username
    print request.session

    if user_id:
        user = session.query(User) \
                        .filter(User.id == user_id) \
                        .first()
        session.query(User) \
            .filter(User.id == user_id).update({User.last_login: datetime.datetime.now()})
    else:
        user = None
    return user


@subscriber(BeforeRender)
def add_social(event):
    request = event['request']
    event['social'] = backends(request, request.user)
