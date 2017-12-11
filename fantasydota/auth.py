from pyramid.events import subscriber, BeforeRender
from social_core.pipeline.user import create_user
from social_pyramid.utils import backends

from .models import DBSession, User, UserXp


def login_user(backend, user, user_social_auth):
    backend.strategy.session_set('user_id', user.id)


def login_required(request):
    return getattr(request, 'user', None) is not None


# def create_user_with_xp(strategy, details, backend, user=None, *args, **kwargs):
#     '''
#     ran into issues with this
#     if want to use user_id in the league_user tables.
#     How does it know what the user_id is, if its trying to use the user before the commit has finished
#     decided to just make the league in the viewLeague request if needed
#     '''
#     return_dict = create_user(strategy, details, backend, user, *args, **kwargs)
#     user_id = strategy.session_get("user_id")
#     session = DBSession()
#     session.add(UserXp(user_id))
#     return return_dict


def create_userxp_tables(strategy, details, backend, user=None, *args, **kwargs):
    session = DBSession()
    session.add(UserXp(user.id))


def get_user(request):
    session = DBSession()
    user_id = request.session.get('user_id')

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
