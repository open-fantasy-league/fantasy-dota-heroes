import transaction
from fantasydota.lib.session_utils import make_session
from fantasydota.models import League


def end_league():
    with transaction.manager:
        session = make_session()
        transfer_open_league = session.query(League).filter(League.game == 1).filter(League.status == 0).first()
        new_name = "Week " + str(int(transfer_open_league.name.split(" ")[1]) + 1)
        # stage 2 deliberately too high. only want stage1 and stage 3
        new_league = League(1, new_name, 7, 5, 9, "")
        session.add(new_league)
        session.query(League).filter(League.game == 1).filter(League.status == 1).update({League.status: 2})
        transfer_open_league.status = 1  # this is now in play

        transaction.commit()

if __name__ == "__main__":
    end_league()
