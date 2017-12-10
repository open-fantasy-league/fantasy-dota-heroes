import transaction
from fantasydota.lib.account import add_achievement, team_swap_all
from fantasydota.lib.general import match_link
from sqlalchemy import and_

from fantasydota.lib.constants import MULTIPLIER
from fantasydota.lib.session_utils import make_session
from fantasydota.models import Result, LeagueUser, League, LeagueUserDay, \
    TeamHero, Game


def add_results_to_user(session, userq, userq_day, new_results, league_id, team_size, game_id):
    picks = 0
    bans = 0
    heroes = [x[0] for x in session.query(TeamHero.hero_id).filter(and_(TeamHero.league == league_id,
                                                         TeamHero.user_id == userq.user_id)).filter(
            TeamHero.active.is_(True)).all()]
    hero_count = len(heroes)
    match = None
    for result in new_results:
        # This check necessary in-case multiple matches come in at once
        # think I can get away without ordering query by match id
        # because get_tournament_data never running in parallel
        # not possible to get mixed results from two matches
        if match != result.match_id:
            picks = 0
            bans = 0
        match = result.match_id
        if result.hero in heroes:
            res = result.result_str
            user_id = userq.user_id
            if "p" in res:
                picks += 1
                userq.picks += 1
                userq_day.picks += 1
            if "w" in res:
                userq.wins += 1
                userq_day.wins += 1
            if "b" in res:
                bans += 1
                userq.bans += 1
                userq_day.bans += 1
            if game_id == 1:
                to_add = MULTIPLIER * ((0.5 ** (team_size - hero_count)) * Result.result_to_value(res))
            elif game_id == 2:
                to_add = MULTIPLIER * ((0.5 ** (team_size - hero_count)) * Result.result_to_value_pubg(res))
            print "addin %s points to %s" % (to_add, user_id)
            userq.points += to_add
        # Despite looping over all results in match. with equals these can only be awarded once per match
        if picks == 3:
            add_achievement(session, userq.user_id, 'Three of a Kind', match_link(match))
        if picks + bans == 5:
            add_achievement(session, userq.user_id, 'Full House', match_link(match))


def update_league_points(session, league):
    league_id = league.id
    new_results = session.query(Result).filter(Result.applied == 1). \
        filter(Result.tournament_id == league_id).all()

    for userq in session.query(LeagueUser).filter(LeagueUser.league == league_id).all():
        team_size = session.query(Game.team_size).filter(Game.id == league.game).first()[0]
        game = league.game
        userq_day = session.query(LeagueUserDay).filter(and_(LeagueUserDay.user_id == userq.user_id,
                                                             LeagueUserDay.league == userq.league,
                                                             LeagueUserDay.day == league.current_day
                                                             )).first()
        add_results_to_user(session, userq, userq_day, new_results, league_id, team_size, game)

    for res in new_results:
        res.applied = 2


def main():

    with transaction.manager:
        session = make_session()
        for league in session.query(League).all():
            team_swap_all(session, league.id)
            session.flush()
            update_league_points(session, league)
        transaction.commit()

if __name__ == "__main__":
    main()
