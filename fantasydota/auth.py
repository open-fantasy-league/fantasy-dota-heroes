from pyramid.events import subscriber, BeforeRender
from social_pyramid.utils import backends

from .models import DBSession, User


def login_user(backend, user, user_social_auth):
    backend.strategy.session_set('user_id', user.id)


def login_required(request):
    return getattr(request, 'user', None) is not None


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
