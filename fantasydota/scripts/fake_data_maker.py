import random
import transaction
from fantasydota.lib.herolist import heroes
from fantasydota.lib.session_utils import make_session
from fantasydota.models import User, TeamHero, LeagueUser, LeagueUserDay
from fantasydota.scripts.start_of_day import start_of_day


def main():
    session = make_session(False)
    for i in range(16):
        username = "tpaintpaintpaintp" + str(i)
        session.add(User(username, "aaaaaa"))
        session.flush()
        user_id = session.query(User.id).filter(User.username == username).first()[0]
        session.add(LeagueUser(user_id,
                              username, 5157))
        session.flush()
        for i in range(3):
            if i >= 2:
                stage = 2
            elif i >= 0:
                stage = 1
            else:
                stage = 0
            session.add(LeagueUserDay(user_id,
                                      username, 5157, i, stage))
            session.flush()
        for _ in range(5):
            session.add(TeamHero(user_id, random.choice(heroes)["id"], 5157, 20.0))
        session.flush()
    session.commit()

    #start_of_day()

if __name__ == "__main__":
    main()
