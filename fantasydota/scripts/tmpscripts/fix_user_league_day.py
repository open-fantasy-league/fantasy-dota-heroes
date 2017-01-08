import transaction
from fantasydota.lib.session_utils import make_session
from fantasydota.models import League, User, LeagueUser, LeagueUserDay


def main():
    session = make_session()

    with transaction.manager:
        for user in session.query(User).all():
            if session.query(LeagueUserDay).filter(LeagueUserDay.username == user.username).first():
                continue
	    print user.username
            #session.add(LeagueUser(user.username, 5018))
            for i in range(3):
                if i >= 2:
                    stage = 2
                elif i >= 0:
                    stage = 1
                else:
                    stage = 0
                session.add(LeagueUserDay(user.username, 5018, i, stage))
        transaction.commit()

if __name__ == "__main__":
    main()
