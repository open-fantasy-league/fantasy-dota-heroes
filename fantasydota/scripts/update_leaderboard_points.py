import transaction
from fantasydota.lib.account import add_achievement
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
    for result in new_results:
        if result.hero in heroes:
            res = result.result_str
            user_id = userq.user_id
            if "p" in res:
                picks += 1
            if "w" in res:
                userq.wins += 1
                userq_day.wins += 1
            if "b" in res:
                bans += 1
            if game_id == 1:
                to_add = MULTIPLIER * ((0.5 ** (team_size - hero_count)) * Result.result_to_value(res))
            elif game_id == 2:
                to_add = MULTIPLIER * ((0.5 ** (team_size - hero_count)) * Result.result_to_value_pubg(res))
            print "addin %s points to %s" % (to_add, user_id)
            userq.points += to_add
    userq.picks += picks
    userq_day.picks += picks
    userq.bans += bans
    userq_day.bans += bans
    if picks >= 3:
        add_achievement(userq.user_id, 'Three of a Kind')
    if picks + bans == 5:
        add_achievement(userq.user_id, 'Full House')


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
            update_league_points(session, league)
        transaction.commit()

if __name__ == "__main__":
    main()
