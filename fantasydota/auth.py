from pyramid.events import subscriber, BeforeRender
from social_core.pipeline.user import create_user
from social_pyramid.utils import backends

from .models import DBSession, User, LeagueUserDay, LeagueUser, League


def login_user(backend, user, user_social_auth):
    backend.strategy.session_set('user_id', user.id)


def login_required(request):
    return getattr(request, 'user', None) is not None


def create_user_with_league(strategy, details, backend, user=None, *args, **kwargs):
    '''
    ran into issues with this
    if want to use user_id in the league_user tables.
    How does it know what the user_id is, if its trying to use the user before the commit has finished
    decided to just make the league in the viewLeague request if needed
    '''
    return_dict = create_user(strategy, details, backend, user, *args, **kwargs)
    username = kwargs.get("username", details.get("username"))
    user_id = strategy.session_get("user_id")
    session = DBSession()
    leagues = session.query(League).all()
    for l in leagues:
        user_league = LeagueUser(user_id, username, l.id)
        session.add(user_league)
        for i in range(l.days):
            if i >= l.stage2_start:
                stage = 2
            elif i >= l.stage1_start:
                stage = 1
            else:
                stage = 0
            session.add(LeagueUserDay(user_id,username, l.id, i, stage))

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
        # session.query(User) \
        #     .filter(User.id == user_id).update({User.last_login: datetime.datetime.now()})
    else:
        user = None
    return user


@subscriber(BeforeRender)
def add_social(event):
    request = event['request']
    event['social'] = backends(request, request.user)
