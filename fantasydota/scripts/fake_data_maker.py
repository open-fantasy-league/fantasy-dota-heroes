import random
import transaction
from fantasydota.lib.herolist import heroes
from fantasydota.lib.session_utils import make_session
from fantasydota.models import User, TeamHero, LeagueUser, LeagueUserDay
from fantasydota.scripts.start_of_day import start_of_day


def main():
    session = make_session()
    with transaction.manager:
        for i in range(16):
            username = "tpain" + str(i)
            #session.add(User(username, "aaaaaa"))
            session.add(LeagueUser(username, 4979))
            for i in range(3):
                if i >= 2:
                    stage = 2
                elif i >= 0:
                    stage = 1
                else:
                    stage = 0
                session.add(LeagueUserDay(username, 4979, i, stage))
        transaction.commit()
            # with transaction.manager:
            #     for _ in range(5):
            #         session.add(TeamHero(username, random.choice(heroes)["id"], 4979, True))
            #         session.add(TeamHero(username, random.choice(heroes)["id"], 4979, False))
            #     transaction.commit()

    #start_of_day()

if __name__ == "__main__":
    main()
