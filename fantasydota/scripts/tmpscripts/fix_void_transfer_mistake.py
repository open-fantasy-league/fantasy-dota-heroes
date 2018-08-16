import transaction
from fantasydota.lib.hero import calibrate_value
from fantasydota.lib.session_utils import make_session
from fantasydota.models import Hero, LeagueUser, TeamHero
from sqlalchemy import func


def main():
    session = make_session()
    league_id = 9870
    old_values = {}
    with transaction.manager:
        average_points = float(session.query(func.avg(Hero.points)).filter(Hero.league == league_id).scalar())
        heroes = session.query(Hero).filter(Hero.league == league_id)
        for hero in heroes:
            new_calibration = calibrate_value(average_points, hero.points)
            current_value = hero.value
            old_value = (current_value * 10 - new_calibration) / 9
            old_values[hero.id] = old_value

        for luser in session.query(LeagueUser).filter(LeagueUser.league == league_id).filter(
                        LeagueUser.swap_tstamp == None).all():
            for th in session.query(TeamHero).filter(TeamHero.user_id == luser.user_id):
                if not th.active:
                    luser.money += th.cost
                    session.delete(th)
                    luser.voided_transfers = True
                elif th.active and th.reserve:
                    th.reserve = False
                    luser.money -= th.cost
                    luser.voided_transfers = True

        transaction.commit()

if __name__ == "__main__":
    main()