import transaction
from fantasydota.lib.bw_players import bw_players
from fantasydota.lib.herolist_vals import heroes_init
from fantasydota.models import Hero


def create_tables(DBSession):
    session = DBSession()
    with transaction.manager:
        if not session.query(Hero).first():
            for add_hero in bw_players:
                hero = Hero(add_hero["id"], add_hero["name"], add_hero["race"], add_hero["value"], 1, False)
                session.add(hero)
                hero = Hero(add_hero["id"], add_hero["name"], add_hero["race"], add_hero["value"], 1, True)
                session.add(hero)
            transaction.commit()
