from fantasydota.lib.herolist import heroes
from fantasydota.models import Hero, Result
from sqlalchemy import and_
from sqlalchemy import func


def calibrate_all_hero_values(session):
    new_heroes_list = heroes
    for h in new_heroes_list:
        h["points"] = 0
    results = session.query(Result).filter(Result.applied.is_(False)).all()
    sum_points = 0
    print len(results)
    import pdb; pdb.set_trace()
    for res in results:
        points = Result.result_to_value(res.result_str)
        [hero for hero in new_heroes_list if hero["id"] == res.hero][0]["points"] += points
        sum_points += points
    print sum_points
    average_points = sum_points / len(new_heroes_list)
    print "average points", average_points
    sum = 0
    i = 0
    for hero in new_heroes_list:
        print hero["name"], hero["points"]
        if hero["points"] < 0:
            hero["points"] = 1
        value = calibrate_value(average_points, hero["points"])
        for hero_d in new_heroes_list:
            if hero_d["id"] == hero["id"]:
                hero_d["value"] = round(value, 1)
                print "New %s: %s" % (hero_d["name"], round(value, 1))
        sum += value
        i += 1

    print "Average new value:", sum / i
    with open("/home/jdog/bin/seovenv/bin/fantasydota/fantasydota/lib/herolist_vals.py", 'w+') as f:
        f.write("heroes_init = " + repr(new_heroes_list))


def calibrate_value(average_points, our_points):
    # was (10. * (our_points / average_points) * 0.85 * 4 + 8.5) / 5. for boston
    # make bit higher for esl genting because so unknown whats going to happen.
    return ((float(our_points) / float(average_points)) * 8.5 * 3 + 8.5) / 4.


def combine_calibrations(older_value, newer_value):
    return (newer_value + older_value) * 0.75/ 2.


def recalibrate_bcup_hero_values(session, league_id):
    heroes = session.query(Hero).filter(and_(Hero.is_battlecup.is_(True),
                                             Hero.league == league_id,
                                        ))
    average_points = float(session.query(func.avg(Hero.points)).filter(and_(
       Hero.is_battlecup.is_(True), Hero.league == league_id
    )).scalar())
    for hero in heroes:
        new_calibration = calibrate_value(average_points, hero.points)
        print "new calbration: %s, from %s" % (new_calibration, hero.value)
        hero.value = round(combine_calibrations(hero.value, new_calibration), 1)
