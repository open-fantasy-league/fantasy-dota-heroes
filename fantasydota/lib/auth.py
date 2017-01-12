from pyramid.security import authenticated_userid


def get_user(request):
    #user_id = request.session.get('user_id')
    return authenticated_userid(request)