import transaction
from tutorial.lib.herolist_vals import heroes_init
from tutorial.models import Hero


def create_tables(DBSession):
    session = DBSession()
    with transaction.manager:
        if not session.query(Hero).first():
            for add_hero in heroes_init:
                hero = Hero(add_hero["id"], add_hero["name"], add_hero["value"])
                session.add(hero)
            transaction.commit()
