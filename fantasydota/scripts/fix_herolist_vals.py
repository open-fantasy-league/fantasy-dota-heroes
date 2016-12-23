import transaction
from fantasydota.lib.herolist_vals import heroes_init
from fantasydota.lib.session_utils import make_session
from fantasydota.models import Hero


def main():
    session = make_session()
    with transaction.manager:
        heroesq = session.query(Hero).all()
        new_heroes_list = heroes_init
        for hero in heroesq:
            for hero_d in new_heroes_list:
                if hero_d["id"] == hero.hero_id:
                    hero_d["value"] = hero.value
        # "/home/johnny/env/bin/fantasydota/fantasydota/lib/herolist_vals.py"
        with open("/home/johnny/env/bin/fantasydota/fantasydota/lib/herolist_vals.py", 'w+') as f:
            f.write("heroes_init = " + repr(new_heroes_list))
        transaction.commit()

if __name__ == "__main__":
    main()