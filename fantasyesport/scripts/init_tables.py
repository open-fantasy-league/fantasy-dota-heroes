import transaction
from fantasyesport.lib.bw_players import bw_players
from fantasyesport.models import Hero


def create_tables(DBSession):
    with transaction.manager:
        session = DBSession()
        if not session.query(Hero).first():
            for add_hero in bw_players:
                hero = Hero(add_hero["id"], add_hero["name"], add_hero["race"], add_hero["value"], 1, False)
                session.add(hero)
                hero = Hero(add_hero["id"], add_hero["name"], add_hero["race"], add_hero["value"], 1, True)
                session.add(hero)
            transaction.commit()
