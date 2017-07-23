import transaction
from fantasydota.lib.herolist_vals import heroes_init
from fantasydota.models import Hero


def create_tables(DBSession):
    session = DBSession()
    with transaction.manager:
        if not session.query(Hero).filter(Hero.league == 5401).first():
            for add_hero in heroes_init:
                hero = Hero(add_hero["id"], add_hero["name"], add_hero["value"], 5401)
                session.add(hero)
            transaction.commit()
