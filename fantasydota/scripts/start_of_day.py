import transaction
from fantasydota.lib.battlecup import make_battlecups
from fantasydota.lib.session_utils import make_session
from fantasydota.models import League, TeamHero
from sqlalchemy import and_


def start_of_day():
    session = make_session()
    for league in session.query(League).filter(League.status == 1).all():
        rounds = 4  # temp
        series_per_round = "2,1,1,1"
        players = session.query(TeamHero.user).\
            filter(and_(TeamHero.is_battlecup.is_(True),
                        TeamHero.league == league.id)).group_by(TeamHero.user).all()
        print len(players)
        make_battlecups(session, league.id, rounds, players, series_per_round)
        league.battlecup_status = 1  # switch bcup view to bracket


def main():
    start_of_day()

if __name__ == "__main__":
    main()
