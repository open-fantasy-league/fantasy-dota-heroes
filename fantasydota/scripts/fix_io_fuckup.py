import transaction
from sqlalchemy import and_
from sqlalchemy import desc
from fantasydota.lib.session_utils import make_session
from fantasydota.models import Hero, Result, TeamHero, User, BattlecupUser, BattlecupUserPoints, Battlecup



def update_hero_values(session):
    with transaction.manager:

        users = session.query(TeamHero).\
        filter(and_(TeamHero.active == True, TeamHero.hero == 91)).all()
        for user_res in users:
            userq = session.query(User).filter(User.username == user_res.username).first()
            userq.bans -= 1
            #userq.points -= (0.5 ** (5 - userq.hero_count)) * 2
            print "would remove %s points" % (0.5 ** (5 - userq.hero_count)) * 2

        transaction.commit()


def main():
    session = make_session()
    update_hero_values(session)

if __name__ == "__main__":
    main()
