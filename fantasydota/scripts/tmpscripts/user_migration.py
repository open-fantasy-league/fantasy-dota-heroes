import transaction
from fantasydota.lib.session_utils import make_session
from fantasydota.models import User, UserXp, Notification


def migrate_users():
    # https://stackoverflow.com/questions/12242772/easiest-way-to-copy-a-table-from-one-database-to-another#12243188
    # do above first
    session = make_session()
    with transaction.manager:
        for user in session.query(User).all():
            #session.add(UserXp(user.id))
            # session.add(Notification(
            #     user.id, None, 'New profile page where you can earn achievements, Xp and level up', '/profile'
            # ))
            session.add(Notification(
                user.id, None, 'Brand new system! Every pro-circuit match scores points. New league every week starting 2018-01-01 (Pick your team for first week now)', '/team'
            ))
    return

if __name__ == "__main__":
    migrate_users()
