import random

from fantasydota.lib.bw_players import bw_players
from fantasydota.lib.session_utils import make_session
from fantasydota.models import User, TeamHero, LeagueUser, LeagueUserDay


def main():
    session = make_session(False)
    for i in range(16):
        username = "tpaintpaintpaintp" + str(i)
        session.add(User(username, "aaaaaa"))
        session.flush()
        user_id = session.query(User.id).filter(User.username == username).first()[0]
        new_lu = LeagueUser(user_id, username, 1)
        session.add(new_lu)
        session.flush()
        for j in range(3):
            if j >= 2:
                stage = 2
            elif j >= 0:
                stage = 1
            else:
                stage = 0
            session.add(LeagueUserDay(new_lu.id, j, stage))
            session.flush()
        for _ in range(5):
            session.add(TeamHero(user_id, random.choice(bw_players)["id"], 1, True, 1, 20.0))
            session.add(TeamHero(user_id, random.choice(bw_players)["id"], 1, False, random.randint(1, 5), 20.0))
        session.flush()
    session.commit()

    # session.add(User("FAKE_USER_FOR_BATTLECUP", "aaaaaa"))
    # session.flush()
    #start_of_day()

if __name__ == "__main__":
    main()
