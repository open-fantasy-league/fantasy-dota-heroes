import transaction
from fantasydota.lib.battlecup import make_battlecups
from fantasydota.lib.hero import recalibrate_bcup_hero_values
from fantasydota.lib.session_utils import make_session
from fantasydota.models import League, TeamHero, BattlecupTeamHeroHistory, BattlecupRound, Battlecup
from fantasydota.scripts.update_hero_values import declare_bcup_rounds_winners
from sqlalchemy import and_


def main():
    session = make_session()
    with transaction.manager:
        for league in session.query(League).filter(League.status == 1).all():
            bcup_teams = session.query(TeamHero).filter(and_(TeamHero.league == league.id,
                                                                   TeamHero.is_battlecup == True)).all()
            for bcup_team in bcup_teams:
                session.add(BattlecupTeamHeroHistory(bcup_team.user, bcup_team.hero_id, league.id, league.current_day))
            for bcup_round in session.query(BattlecupRound).filter(BattlecupRound.winner == 0).all():
                declare_bcup_rounds_winners(session, bcup_round)
            session.query(Battlecup).filter(Battlecup.day == league.current_day).update({
                Battlecup.current_round: Battlecup.current_round + 1
            })
            session.query(TeamHero).filter(and_(TeamHero.league == league.id,
                                                TeamHero.is_battlecup == True)).delete()
            if league.id == 49795:
                recalibrate_bcup_hero_values(session, league.id)
            league.current_day += 1
            league.battlecup_status = 0  # switch bcup view to pick team view
        transaction.commit()

if __name__ == "__main__":
    main()
