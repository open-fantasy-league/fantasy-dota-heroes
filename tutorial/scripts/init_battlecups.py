import transaction
from tutorial.lib.session_utils import make_session
from tutorial.models import User, Battlecup, BattlecupUser


def main():
    session = make_session()
    with transaction.manager:
        users = session.query(User).all()
        users_num = len(users)
        cups = (users_num / 8)
        if users_num % 8 != 0:
            cups += 1
        for i in range(cups):
            with transaction.manager:
                session.add(Battlecup(3, 0))
                transaction.commit()
        cup_counter = 1
        with transaction.manager:
            for user in users:
                if cup_counter > cups:
                    cup_counter = 1
                session.add(BattlecupUser(cup_counter, user.username, user.user_id))
                cup_counter += 1
            transaction.commit()

if __name__ == "__main__":
    main()
