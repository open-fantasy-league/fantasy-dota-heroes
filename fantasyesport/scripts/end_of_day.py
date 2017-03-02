import transaction
from fantasyesport.lib.hero import recalibrate_hero_values
from fantasyesport.lib.session_utils import make_session
from fantasyesport.models import League, TeamHero, BattlecupTeamHeroHistory, BattlecupRound, Battlecup
from fantasyesport.scripts.update_battlecups import declare_bcup_rounds_winners
from sqlalchemy import and_


def main():
    with transaction.manager:
        session = make_session()
        for league in session.query(League).all():
            bcup_teams = session.query(TeamHero).filter(and_(TeamHero.league == league.id,
                                                                   TeamHero.is_battlecup.is_(True))).all()
            for bcup_team in bcup_teams:
                session.add(BattlecupTeamHeroHistory(bcup_team.user_id, bcup_team.hero_id, league.id, league.current_day))
            for bcup_round in session.query(BattlecupRound).filter(BattlecupRound.winner == 0).all():
                declare_bcup_rounds_winners(session, bcup_round)
            session.query(Battlecup).filter(Battlecup.day == league.current_day).update({
                Battlecup.current_round: Battlecup.current_round + 1
            })
            # Clear battlecup teams
            session.query(TeamHero).filter(and_(TeamHero.league == league.id,
                                                TeamHero.is_battlecup.is_(True))).delete()

            # Remove loaned heroes from team whos loan run out
            session.query(TeamHero).filter(and_(TeamHero.league == league.id,
                                                TeamHero.days_left == 1,
                                                TeamHero.is_battlecup.is_(False))).delete()
            # Decrement all remaining loan heroes days left
            session.query(TeamHero).filter(and_(TeamHero.league == league.id,
                                                TeamHero.is_battlecup.is_(False))).\
                update({TeamHero.days_left: TeamHero.days_left - 1})

            # recalibrate_hero_values(session, league.id) not doing this for bw. too short tournament
            league.current_day += 1
            league.battlecup_status = 0  # switch bcup view to pick team view
            league.transfer_open = True
        transaction.commit()

if __name__ == "__main__":
    main()
