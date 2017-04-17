import transaction

from fantasydota.lib.session_utils import make_session
from fantasydota.models import OldFriend, Friend, User


def main():
    session = make_session()
    with transaction.manager:
        old_friends = session.query(OldFriend).all()
        for old in old_friends:
            username = old.user
            friend_username = old.friend
            user_id = session.query(User.id).filter(User.username == username).first()[0]
            friend_id = session.query(User.id).filter(User.username == friend_username).first()[0]
            new_friend = Friend(user_id, friend_id)
            session.add(new_friend)
        transaction.commit()

if __name__ == "__main__":
    main()
