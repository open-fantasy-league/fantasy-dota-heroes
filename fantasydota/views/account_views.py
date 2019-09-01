import datetime
from urllib import quote_plus

from fantasydota import DBSession
from fantasydota.auth import get_user
from fantasydota.lib.constants import FESPORT_ACCOUNT
from fantasydota.lib.general import all_view_wrapper
from fantasydota.models import User, PasswordReset, Notification
from passlib.handlers.bcrypt import bcrypt
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.security import remember, forget, authenticated_userid
from pyramid.view import view_config
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

def check_invalid_password(password, confirm_password):
    if len(password) < 6:
        return {"message": "Password too short. 6 characters minimum please"}
    elif len(password) > 20:
        return {"message": "Password too long. 20 characters maximum please"}
    elif confirm_password != password:
        return{"message": "Passwords did not match"}
    else:
        return False


@view_config(route_name='login', renderer='../templates/login.mako')
def login(request):
    session = DBSession()
    message = request.params.get('message')
    username = request.params.get('username')
    if request.method == 'POST':
        if username:
            # Think now have steam accounts. can have different accounts but same name
            userq = session.query(User).filter(User.username == username).\
                filter(User.account_type == FESPORT_ACCOUNT).all()
            if not userq:
                message = "Username not recognised (did you previously log in through steam or reddit?)"
            else:
                for user in userq:
                    if user.validate_password(request.params.get('password')):
                        headers = remember(request, user.id)
                        user.last_login = datetime.datetime.now()
                        return HTTPFound('/team', headers=headers)
                else:
                    headers = forget(request)
                    message = "Password was incorrect"
        else:
            message = 'Must specify username'
            headers = forget(request)
    return_dict = {'message': message, "plus_id": request.registry.settings.get(
        'SOCIAL_AUTH_STEAM_KEY'
    )}
    return all_view_wrapper(request, return_dict, session)


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location='/login', headers=headers)


@view_config(route_name='register')
def register(request):
    session = DBSession()
    username = request.params.get('username')
    password = request.params.get('password')
    confirm_password = request.params.get('confirm_password')
    email = request.params.get('email')
    user = session.query(User).filter(User.username == username).\
        filter(User.account_type == FESPORT_ACCOUNT).first()
    if user:
        params = {"message": "Username already in use"}
        return HTTPFound(location=request.route_url('login', _query=params))

    if len(username) < 3:
        params = {"message": "Username too short"}
        return HTTPFound(location=request.route_url('login', _query=params))
    elif len(username) > 20:
        params = {"message": "Username too long (20 characters max)"}
        return HTTPFound(location=request.route_url('login', _query=params))
    elif not username.replace(" ", "").isalnum():
        params = {"message": "Only letters and numbers in username please."}
        return HTTPFound(location=request.route_url('login', _query=params))

    pword_invalid_check = check_invalid_password(password, confirm_password)
    if pword_invalid_check:
        return HTTPFound(location=request.route_url('login', _query=pword_invalid_check))

    user = User(username, password, email, ip_address=request.remote_addr)
    session.add(user)
    session.flush()
    headers = remember(request, user.id)
    return HTTPFound('/team', headers=headers)


@view_config(route_name='change_password')
def change_password(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    new_password = request.params.get('new_password')
    confirm_new_password = request.params.get('confirm_new_password')
    old_password = request.params.get('old_password')
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        params = {"message": "Your username could not be found",
                  "message_type": "change_password"}
        return HTTPFound(location=request.route_url('account_settings', _query=params))

    if not user.validate_password(old_password):
        params = {"message": "Old password did not match",
                  "message_type": "change_password"}
        return HTTPFound(location=request.route_url('account_settings', _query=params))

    if old_password == "":  # this is the case for steam accounts
        params = {"message": "Change password does not apply to steam logins",
                  "message_type": "failure"}
        return HTTPFound(location=request.route_url('account_settings', _query=params))

    pword_invalid_check = check_invalid_password(new_password, confirm_new_password)
    if pword_invalid_check:
        return HTTPFound(location=request.route_url('account_settings', _query=pword_invalid_check))

    session.query(User).filter(User.id == user_id).update({User.password: bcrypt.encrypt(new_password)})
    params = {"message": "Congratulations! Password successfully changed",
                  "message_type": "success"}
    return HTTPFound(location=request.route_url('account_settings', _query=params))


@view_config(route_name='forgot_password', renderer='../templates/reset_password_email.mako')
def forgot_password(request):
    session = DBSession()
    username = request.params.get('username').lower() if request.params.get('username') else None
    email = request.params.get('email').lower() if request.params.get('email') else None
    userq = session.query(User).filter(User.username == username).filter(User.email == email).\
        filter(User.account_type == FESPORT_ACCOUNT).first()
    return_dict = None
    if not username or not userq:
        return_dict = {"message": "Username and email for password reset did not match. Please check filled in correctly"}
        return all_view_wrapper(request, return_dict, session)
    elif not userq.email:
        return_dict = {"message": "Sorry you did not have an email address associated with this account. Please email fantasydotaeu@gmail.com directly"}
        return all_view_wrapper(request, return_dict, session)
    guid = bcrypt.encrypt(str(userq.id))
    tries = session.query(PasswordReset).filter(PasswordReset.time > datetime.datetime.now() - datetime.timedelta(days=1)).filter(PasswordReset.user_id == userq.id).count()
    if tries > 1:
        return_dict = {"message": "You have already tried 2 password resets today. Please email directly if still having issues"}
        return all_view_wrapper(request, return_dict, session)
    try:
        session.add(PasswordReset(userq.id, guid, request.remote_addr))
        email_url = "https://www.fantasydota.eu/resetPasswordPage?u=" + str(userq.id) + "&guid="  # how not hardcode domain bit?
        email_url += quote_plus(guid)
        message = Message(subject="Open fantasu league password reset",
                          sender="Open Fantasy League",
                          recipients=[userq.email],
                          body="Hi %s.\n\nIf you did not request a password reset, either ignore this email or report incident to me.\n\n"
                               "Otherwise please click this link to reset: %s\n\nThis link will expire in 24 hours" % (userq.username, email_url))
        mailer = get_mailer(request)
        mailer.send(message)
    except:
        return_dict = {"message": "Unexpected error occurred when sending reset email"}
    if not return_dict:
        return_dict = {"message": "Instructions for password reset have been emailed to you",
                "message_type": "success"}
    return all_view_wrapper(request, return_dict, session, userq.user_id)


@view_config(route_name='reset_password_page', renderer='../templates/reset_password.mako')
def reset_password_page(request):
    session = DBSession()
    guid = request.params.get('guid')
    user_id = request.params.get('u')
    reset = session.query(PasswordReset).filter(PasswordReset.user_id == user_id).first()
    if not reset.validate_guid(guid):
        raise HTTPForbidden()
    else:
        # Link is over 24 hours old
        if reset.time + datetime.timedelta(days=1) < datetime.datetime.now():
            raise HTTPForbidden()
        return_dict = {"guid": guid}
        return all_view_wrapper(request, return_dict, session, user_id)


@view_config(route_name='reset_password')
def reset_password(request):
    session = DBSession()
    guid = request.params.get('guid')
    user_id = request.params.get('user_id')
    new_password = request.params.get('new_password')
    confirm_new_password = request.params.get('confirm_new_password')
    if not session.query(PasswordReset).filter(PasswordReset.user_id == user_id).first().validate_guid(guid):
        raise HTTPForbidden()

    if confirm_new_password != new_password:
        params = {"message": "Passwords did not match",
                  "message_type": "change_password"}
        return HTTPFound(location=request.route_url('viewAccount', _query=params))

    pword_invalid_check = check_invalid_password(new_password, confirm_new_password)
    if pword_invalid_check:
        return HTTPFound(location=request.route_url('login', _query=pword_invalid_check))

    session.query(User).filter(User.id == user_id).update({User.password: bcrypt.encrypt(new_password)})
    session.query(PasswordReset).filter(PasswordReset.user_id == user_id).delete()
    params = {"message": "Congratulations! Password successfully changed",
              "message_type": "success"}
    return HTTPFound(location=request.route_url('login', _query=params))


@view_config(route_name='account_settings', renderer="../templates/account_settings.mako")
def account_settings(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if not user_id:
        return HTTPFound('/login')
    message = request.params.get("message")
    message_type = request.params.get("message_type")
    return_dict = {"message": message, "message_type": message_type}
    return all_view_wrapper(request, return_dict, session, user_id)


@view_config(route_name='update_email_settings')
def update_email_settings(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if not user_id:
        return HTTPFound('/login')
    new_email = request.params.get('email')
    contactable = True if request.params.get('emailContact') == "on" else False
    session.query(User).filter(User.id == user_id).\
        update({User.contactable: contactable, User.email: new_email})
    params = {"message": "Congratulations! Email settings successfully updated",
              "message_type": "success"}
    return HTTPFound(location=request.route_url('account_settings', _query=params))


@view_config(route_name='clear_notifications', renderer='string')
def clear_notifications(request):
    session = DBSession()
    user_id = authenticated_userid(request)
    if not user_id:
        return HTTPForbidden()
    session.query(Notification).filter(Notification.user == user_id).update({
        Notification.seen: True
    })
    return 'Marked notifications as seen'


# @view_config(route_name='home', renderer='../templates/login.mako')
# def home(request):
#     try:
#         user = get_user(request)
#         headers = remember(request, user.id)
#         return HTTPFound("/team", headers=headers)
#     except:
#         return HTTPFound("/login")
#     # return common_context(
#     #     request.registry.settings['SOCIAL_AUTH_AUTHENTICATION_BACKENDS'],
#     #     load_strategy(request),
#     #     user=get_user(request),
#     #     plus_id=request.registry.settings.get(
#     #         'SOCIAL_AUTH_GOOGLE_PLUS_KEY'
#     #     ),
#     # )


@view_config(route_name='done')
def done(request):
    user = get_user(request)
    headers = remember(request, user.id)
    return HTTPFound('/team', headers=headers)
    # return {"user": get_user(request),
    #         "plus_id": request.registry.settings.get(
    #             'SOCIAL_AUTH_STEAM_KEY'
    #         ),
    #         }
    # return common_context(
    #     request.registry.settings['SOCIAL_AUTH_AUTHENTICATION_BACKENDS'],
    #     load_strategy(request),
    #     user=get_user(request),
    #     plus_id=request.registry.settings['SOCIAL_AUTH_GOOGLE_PLUS_KEY'],
    # )
