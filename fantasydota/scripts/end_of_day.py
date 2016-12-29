import transaction
from fantasydota.lib.battlecup import make_battlecups
from fantasydota.lib.session_utils import make_session
from fantasydota.models import League, TeamHero, BattlecupTeamHeroHistory
from sqlalchemy import and_


def main():
    session = make_session()
    with transaction.manager:
        for league in session.query(League).filter(League.status == 1).all():
            league.current_day += 1
            bcup_teams = session.query(TeamHero).filter(and_(TeamHero.league == league.id,
                                                                   TeamHero.is_battlecup == True)).all()
            for bcup_team in bcup_teams:
                session.add(BattlecupTeamHeroHistory(bcup_team.user, bcup_team.hero_id, league.id, league.current_day))

            bcup_teams.delete()
            league.current_day += 1
            league.battlecup_status = 0  # switch bcup view to pick team view
        transaction.commit()

if __name__ == "__main__":
    main()
