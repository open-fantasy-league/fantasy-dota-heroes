import transaction
from fantasydota.lib.herolist_vals import heroes_init
from fantasydota.models import Hero


def create_tables(DBSession):
    session = DBSession()
    with transaction.manager:
        if not session.query(Hero).first():
            for add_hero in heroes_init:
                hero = Hero(add_hero["id"], add_hero["name"], add_hero["value"], 4874, False)
                session.add(hero)
                hero = Hero(add_hero["id"], add_hero["name"], add_hero["value"] + 10., 4979, False)
                session.add(hero)
                hero = Hero(add_hero["id"], add_hero["name"], add_hero["value"], 4874, True)
                session.add(hero)
                hero = Hero(add_hero["id"], add_hero["name"], add_hero["value"] + 10., 4979, True)
                session.add(hero)
            transaction.commit()
