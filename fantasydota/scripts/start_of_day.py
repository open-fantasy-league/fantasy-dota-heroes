import transaction
from fantasydota.lib.battlecup import make_battlecups, auto_fill_teams
from fantasydota.lib.session_utils import make_session
from fantasydota.models import League, TeamHero
from sqlalchemy import and_


def start_of_day():
    session = make_session(transaction=False, autoflush=False)
    for league in session.query(League).all():  # .filter(League.status == 1)
        # rounds = 4  # temp
        # series_per_round = "1,1,1,1"
        # session.query(TeamHero).filter(and_(TeamHero.is_battlecup.is_(False),
        #                                     TeamHero.league == league.id,
        #                                     )).update({TeamHero.active: True})
        # auto_fill_teams(session, league)
        # players = session.query(TeamHero.user_id).\
        #     filter(and_(TeamHero.is_battlecup.is_(True),
        #                 TeamHero.league == league.id)).group_by(TeamHero.user_id).all()
        # make_battlecups(session, league.id, rounds, players, series_per_round)
        session.query(League).filter(League.id == league.id).update({
            League.battlecup_status: 1, League.transfer_open: 0
        })
        league.battlecup_status = 1  # switch bcup view to bracket
        league.transfer_open = False  # close league window if not already closed
    session.commit()


def main():
    start_of_day()

if __name__ == "__main__":
    main()
