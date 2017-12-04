import transaction
from fantasydota.lib.session_utils import make_session
from fantasydota.models import League
from fantasydota.scripts.add_league import add_league
from fantasydota.scripts.calibrate_values import calibrate_values


def rollover_league():
    calibrate_values()
    with transaction.manager:
        session = make_session()
        transfer_open_league = session.query(League).filter(League.game == 1).filter(League.status == 0).first()
        new_name = "Week " + str(int(transfer_open_league.name.split(" ")[1]) + 1) if transfer_open_league else "Week 1"
        # stage 2 deliberately too high. only want stage1 and stage 3
        new_id = transfer_open_league.id + 1 if transfer_open_league else 1
        add_league(1, new_id, new_name, 7, 5, 9, "", session=session)
        session.query(League).filter(League.game == 1).filter(League.status == 1).update({League.status: 2})
        transfer_open_league.status = 1  # this is now in play

        transaction.commit()

if __name__ == "__main__":
    rollover_league()
