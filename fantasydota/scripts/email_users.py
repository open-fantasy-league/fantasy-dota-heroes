from fantasydota.lib.session_utils import make_session
from fantasydota.models import User
from pyramid_mailer import Mailer
from pyramid_mailer.message import Message


def email_users():
    session = make_session()
    for user in session.query(User).filter(User.email.isnot("")).all():
        if user.email:
            email = "testemail"#user.email
            mailer = Mailer()
            message = Message(subject="Fantasy Hero Dota New System",
                              sender="Fantasy Dota EU",
                              recipients=[email],
                              body="Hi %s.\n\nJust letting you know fantasy leagues now run every week, on all pro circuit matches\n\n"
                                   "You can pick your team for first week starting 1st January now https://www.fantasyesport.eu/dota/team\n\n"
                                   "This is the 'finalised' state of the site for DotA. Therefore I will not email anyone again. Apologies for the spam/promotion. Have a nice Christmas :D" % (
                                   user.username))
            mailer.send(message)
    return

if __name__ == '__main__':
    email_users()
