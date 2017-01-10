import datetime
from urllib import quote_plus

import transaction
from fantasydota import DBSession
from fantasydota.lib.account import check_invalid_password
from fantasydota.models import User, LeagueUser, League, PasswordReset, LeagueUserDay
from passlib.handlers.bcrypt import bcrypt
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.security import remember, forget, authenticated_userid
from pyramid.view import view_config
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from sqlalchemy import func


@view_config(route_name='login', renderer='../templates/login.mako')
def login(request):
    session = DBSession()
    message = request.params.get('message')
    username = request.params.get('username')
    if request.method == 'POST':
        if username:
            username = username.lower()
            userq = session.query(User).filter(User.username == username)
            user = userq.first()
            if user:
                if user.validate_password(request.params.get('password')):
                    headers = remember(request, user.username)
                    userq.update({User.last_login: datetime.datetime.now()})
                    return HTTPFound('/viewLeague', headers=headers)
                else:
                    headers = forget(request)
                    message = "Password did not match stored value for %s" % user.username
            else:
                message = "Username not recognised"
        else:
            message = 'Oops! SOmething went wrong'
            headers = forget(request)
    return {'message': message}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location='/login', headers=headers)


@view_config(route_name='register')
def register(request):
    session = DBSession()
    username = request.params.get('username').lower()
    password = request.params.get('password')
    confirm_password = request.params.get('confirm_password')
    email = request.params.get('email')
    user = session.query(User).filter(User.username == username).first()
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

    user = User(username, password, email)
    session.add(user)
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
            session.add(LeagueUserDay(user.username, l.id, i, stage))
    headers = remember(request, user.username)
    return HTTPFound('/viewLeague', headers=headers)


@view_config(route_name='change_password')
def change_password(request):
    session = DBSession()
    username = authenticated_userid(request)
    new_password = request.params.get('new_password')
    confirm_new_password = request.params.get('confirm_new_password')
    old_password = request.params.get('old_password')
    user = session.query(User).filter(User.username == username).first()
    if not user:
        params = {"message": "Your username could not be found",
                  "message_type": "change_password"}
        return HTTPFound(location=request.route_url('account_settings', _query=params))

    if not user.validate_password(old_password):
        params = {"message": "Old password did not match",
                  "message_type": "change_password"}
        return HTTPFound(location=request.route_url('account_settings', _query=params))

    pword_invalid_check = check_invalid_password(new_password, confirm_new_password)
    if pword_invalid_check:
        return HTTPFound(location=request.route_url('account_settings', _query=pword_invalid_check))

    session.query(User).filter(User.username == username).update({User.password: bcrypt.encrypt(new_password)})
    params = {"message": "Congratulations! Password successfully changed",
                  "message_type": "success"}
    return HTTPFound(location=request.route_url('account_settings', _query=params))


@view_config(route_name='forgot_password', renderer='../templates/login.mako')
def forgot_password(request):
    session = DBSession()
    username = request.params.get('username').lower() if request.params.get('username') else None
    userq = session.query(User).filter(User.username == username).first()
    if not username or not userq:
        return {"message": "Username for password reset did not match. Please check filled in correctly"}
    elif not userq.email:
        return {"message": "Sorry you did not have an email address associated with this account. Please email fantasydotaeu@gmail.com directly"}

    guid = bcrypt.encrypt(str(userq.id))
    if session.query(func.count(PasswordReset)).filter(PasswordReset.time > datetime.datetime.now() - datetime.timedelta(days=1)).\
        scalar() > 2:
        return {"message": "You have already tried 2 password resets today. Please email directly if still having issues"}
    try:
        session.add(PasswordReset(userq.id, guid, request.remote_addr))
        email_url = "https://www.fantasydota.eu/resetPasswordPage?u=" + str(userq.id) + "&guid="  # how not hardcode domain bit?
        email_url += quote_plus(guid)
        message = Message(subject="Fantasy Dota EU password reset",
                          sender="fantasydotaeu@gmail.com",
                          recipients=[userq.email],
                          body="Hi %s.\n\nIf you did not request a password reset, either ignore this email or report incident to me.\n\n"
                               "Otherwise please click this link to reset: %s\n\nThis link will expire in 24 hours" % (userq.username, email_url))
        mailer = get_mailer(request)
        mailer.send(message)
    except:
        return {"message": "Unexpected error occurred when sending reset email"}
    return {"message": "Instructions for password reset have been emailed to you",
            "message_type": "success"}


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
        return {"guid": guid, "user_id": user_id}


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
    username = authenticated_userid(request)
    if not username:
        return HTTPFound('/login')
    message = request.params.get("message")
    message_type = request.params.get("message_type")
    user = session.query(User).filter(User.username == username).first()
    return {"user": user, "message": message, "message_type": message_type}


@view_config(route_name='update_email_settings')
def update_email_settings(request):
    session = DBSession()
    username = authenticated_userid(request)
    if not username:
        return HTTPFound('/login')
    new_email = request.params.get('email')
    contactable = True if request.params.get('emailContact') == "on" else False
    session.query(User).filter(User.username == username).\
        update({User.contactable: contactable, User.email: new_email})
    params = {"message": "Congratulations! Email settings successfully updated",
              "message_type": "success"}
    return HTTPFound(location=request.route_url('account_settings', _query=params))


@view_config(route_name='update_game_settings')
def update_game_settings(request):
    session = DBSession()
    username = authenticated_userid(request)
    if not username:
        return HTTPFound('/login')
    autofill = True if request.params.get('autofillTeam') == "on" else False
    session.query(User).filter(User.username == username).\
        update({User.autofill_team: autofill})
    params = {"message": "Update successful",
              "message_type": "success"}
    return HTTPFound(location=request.route_url('account_settings', _query=params))
