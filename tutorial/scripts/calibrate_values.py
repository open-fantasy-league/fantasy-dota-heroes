from sqlalchemy import func
from tutorial.lib.herolist import heroes
from tutorial.lib.session_utils import make_session
from tutorial.models import Hero


def main():
    session = make_session()

    average_points = float(session.query(func.avg(Hero.points)).first()[0])
    print "average points", average_points
    heroesq = session.query(Hero).all()
    new_heroes_list = heroes
    sum = 0
    i = 0
    for hero in heroesq:
        if hero.points < 0:
            hero.points = 1
        value = (10. * (hero.points /average_points) * 0.85 * 4 + 8.5) / 5.
        for hero_d in new_heroes_list:
            if hero_d["id"] == hero.hero_id:
                hero_d["value"] = round(value, 1)
        sum += value
        i += 1
    print "Average new value:", sum / i
    # "/home/johnny/env/bin/tutorial/tutorial/lib/herolist_vals.py"
    with open("/home/jdog/bin/seovenv/bin/tutorial/tutorial/lib/herolist_vals.py", 'w+') as f:
        f.write("heroes_init = " + repr(new_heroes_list))

if __name__ == "__main__":
    main()
