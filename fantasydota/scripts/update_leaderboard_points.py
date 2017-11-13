import transaction
from sqlalchemy import and_
from sqlalchemy import func

from fantasydota.lib.constants import MULTIPLIER
from fantasydota.lib.session_utils import make_session
from fantasydota.models import Result, LeagueUser, League, LeagueUserDay, \
    TeamHero, Game


def add_result_to_user(userq, res, hero_count, team_size, game_id):
    user_id = userq.user_id
    if "p" in res:
        userq.picks += 1
    if "w" in res:
        userq.wins += 1
    if "b" in res:
        userq.bans += 1
    if game_id == 1:
        to_add = MULTIPLIER * ((0.5 ** (team_size - hero_count)) * Result.result_to_value(res))
    elif game_id == 2:
        to_add = MULTIPLIER * ((0.5 ** (team_size - hero_count)) * Result.result_to_value_pubg(res))
    print "addin %s points to %s" % (to_add, user_id)
    userq.points += to_add


def update_league_points(session, league):
    league_id = league.id
    new_results = session.query(Result).filter(Result.applied == 1). \
        filter(Result.tournament_id == league_id).all()

    for i, result in enumerate(new_results):
        res = result.result_str
        winners = session.query(TeamHero.user_id). \
            filter(and_(TeamHero.hero_id == result.hero, TeamHero.league == league_id)).filter(TeamHero.reserve.is_(False))\
            .all()
        for winner in winners:
            userq = session.query(LeagueUser).filter(and_(LeagueUser.user_id == winner[0],
                                                          LeagueUser.league == league_id)).first()
            user_id = userq.user_id
            userq_day = session.query(LeagueUserDay).filter(and_(LeagueUserDay.user_id == user_id,
                                                            LeagueUserDay.league == userq.league,
                                                            LeagueUserDay.day == league.current_day
                                                                 )).first()
            hero_count = session.query(TeamHero).filter(and_(TeamHero.league == league_id,
                                                                         TeamHero.user_id == user_id)).filter(TeamHero.reserve.is_(False)).count()

            team_size = session.query(Game.team_size).filter(Game.id == league.game).first()[0]
            game = league.game
            add_result_to_user(userq, res, hero_count, team_size, game)
            add_result_to_user(userq_day, res, hero_count, team_size, game)

        result.applied = 2


def main():
    with transaction.manager:
        session = make_session()
        for league in session.query(League).all():
            update_league_points(session, league)
        transaction.commit()

if __name__ == "__main__":
    main()
