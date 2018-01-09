import time
import transaction
from fantasydota.lib.league import close_league
from fantasydota.lib.session_utils import make_session
from fantasydota.models import League, LeagueUser, TeamHero
from fantasydota.scripts.add_league import add_league


def set_late_starters(session, league_id):
    for luser in session.query(LeagueUser).filter(LeagueUser.league == league_id).all():
        if not session.query(TeamHero).filter(TeamHero.league == league_id).filter(TeamHero.user_id == luser.user_id).first():
            luser.late_start = True


def rollover_league():
    with transaction.manager:
        session = make_session()
        transfer_open_league = session.query(League).filter(League.game == 1).filter(League.status == 0).first()
        new_name = "Week " + str(int(transfer_open_league.name.split(" ")[1]) + 1) if transfer_open_league else "Week 1"
        # stage 2 deliberately too high. only want stage1 and stage 3
        new_id = transfer_open_league.id + 1 if transfer_open_league else 1
        # TODO so this will break for new games/non dota
        if new_id > 2:
            close_league(session, 1)

        set_late_starters(session, transfer_open_league.id)
        session.query(League).filter(League.game == 1).filter(League.status == 0).update({League.status: 1,
                                                                                          League.transfer_open: False,
                                                                                          League.swap_open: True,
                                                                                          League.start: time.time()
                                                                                          })
        # recalibration occurs in add_league
        add_league(1, new_id, new_name, 7, 5, 9, "", session=session)

        transfer_open_league.status = 1  # this is now in play

        transaction.commit()

if __name__ == "__main__":
    rollover_league()
