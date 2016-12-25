import transaction
from fantasydota.lib.session_utils import make_session
from fantasydota.models import User
from sqlalchemy import delete


def main():
    """
    Dont want to delete account as soon as indicated. makes battlecupos and stuff awkward.
    so delete it at the end of the day.
    :return:
    """
    session = make_session()
    with transaction.manager:
        delete_accounts = session.query(User.username).filter(User.to_delete == True).all()
        for username in delete_accounts:
            username = username[0]
            # loop over leagues and delete from them
            #session.query(TeamHero).filter(TeamHero.user == username).delete()
            # any others?
            session.query()
        delete(delete_accounts)
        transaction.commit()

if __name__ == "__main__":
    main()
