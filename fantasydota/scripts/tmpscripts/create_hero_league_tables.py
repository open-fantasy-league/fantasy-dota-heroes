import transaction
from fantasydota.lib.herolist_vals import heroes_init
from fantasydota.lib.session_utils import make_session
from fantasydota.models import Hero, HeroLeague, DBSession


def create_tables(session):
    with transaction.manager:
        print "hmmmmm"
        print session.query(HeroLeague).first()
        if not session.query(HeroLeague).first():
            for add_hero in heroes_init:
                print "ello"
                hero = HeroLeague(add_hero["id"], add_hero["name"], add_hero["value"], 4874)
                session.add(hero)
                hero = HeroLeague(add_hero["id"], add_hero["name"], add_hero["value"] + 10., 4979)
                session.add(hero)
            transaction.commit()

if __name__ == "__main__":
    session = make_session()
    create_tables(session)