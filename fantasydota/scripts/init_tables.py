import transaction
from fantasydota.lib.herolist_vals import heroes_init
from fantasydota.models import Hero


def create_tables(DBSession, league_id):
    session = DBSession()
    with transaction.manager:
        if not session.query(Hero).filter(Hero.league == league_id).first():
            for add_hero in heroes_init:
                hero = Hero(add_hero["id"], add_hero["name"], add_hero["value"], league_id)
                session.add(hero)
            transaction.commit()
