import transaction
from fantasyesport.lib.session_utils import make_session
from fantasyesport.models import LeagueUserDay, LeagueUser, BattlecupUser, Battlecup, BattlecupUserRound, \
    BattlecupRound, League


def main():
    session = make_session()
    with transaction.manager:
        LeagueUserDay.__table__.drop()
        transaction.commit()

    with transaction.manager:
        LeagueUser.__table__.drop()
        transaction.commit()

    with transaction.manager:
        BattlecupUserRound.__table__.drop()
        transaction.commit()

    with transaction.manager:
        BattlecupRound.__table__.drop()
        transaction.commit()

    with transaction.manager:
        BattlecupUser.__table__.drop()
        transaction.commit()

    with transaction.manager:
        Battlecup.__table__.drop()
        transaction.commit()

    with transaction.manager:
        League.__table__.drop()
        transaction.commit()

if __name__ == "__main__":
    main()