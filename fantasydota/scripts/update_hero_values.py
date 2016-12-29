import random
import transaction
from fantasydota.lib.session_utils import make_session
from fantasydota.models import Hero, Result, Battlecup, LeagueUser, League, LeagueUserDay, \
    BattlecupUserRound, BattlecupUser, BattlecupRound, TeamHero
from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import or_


def set_user_rankings(session, league_id, day=None):
    # But is there a better way??
    user_l = LeagueUser if day is None else LeagueUserDay
    l_query = session.query(user_l.username).filter(user_l.league == league_id)
    l_query = l_query.filter(user_l.day == day) if day is not None else l_query
    wins_ranking = l_query.order_by(desc(user_l.wins)).all()
    for i, user in enumerate(wins_ranking):
        # try user.wins_rank += 1?
        l_query.filter(user_l.username == user.username).\
            update({user_l.wins_rank: i+1})

    points_ranking = l_query.order_by(desc(user_l.points)).all()
    for i, user in enumerate(points_ranking):
        l_query.filter(user_l.username == user.username). \
            update({user_l.points_rank: i + 1})

    picks_ranking = l_query.order_by(desc(user_l.picks)).all()
    for i, user in enumerate(picks_ranking):
        l_query.filter(user_l.username == user.username). \
            update({user_l.picks_rank: i + 1})

    bans_ranking = l_query.order_by(desc(user_l.bans)).all()
    for i, user in enumerate(bans_ranking):
        l_query.filter(user_l.username == user.username)  . \
            update({user_l.bans_rank: i + 1})
    return


# def update_points(session, result, league_id, day=None):
#     update_points_league(session, result, league_id, day)
#     update_points_battlecup(session, result, league_id)

def add_result_to_user(userq, res, hero_count):
    username = userq.username
    if "p" in res:
        userq.picks += 1
    if "w" in res:
        userq.wins += 1
    if "b" in res:
        userq.bans += 1
    to_add = (0.5 ** (5 - hero_count)) * Result.result_to_value(res)
    print "addin %s points to %s" % (to_add, username)
    userq.points += to_add


def update_league_points(session, result, league_id, day=None):
    res = result.result_str
    winners = session.query(TeamHero.user). \
        filter(and_(TeamHero.hero_id == result.hero, TeamHero.league == league_id,
                    TeamHero.is_battlecup.is_(False))).all()
    for winner in winners:
        userq = session.query(LeagueUser).filter(and_(LeagueUser.username == winner[0],
                                                      LeagueUser.league == league_id)).first()
        if day is not None:
            userq = session.query(LeagueUserDay).filter(and_(LeagueUserDay.username == userq.username,
                                                             LeagueUserDay.league == userq.league,
                                                             LeagueUserDay.day == day
                                                             )).first()
        username = userq.username
        hero_count = session.query(func.count(TeamHero)).filter(and_(TeamHero.league == league_id,
                                                                     TeamHero.user == username,
                                                                     TeamHero.is_battlecup.is_(False))).scalar()
        add_result_to_user(userq, res, hero_count)


def update_battlecup_points(session, result, series_id, bcup_, league_id):
    with transaction.manager:
        bcup = bcup_["bcup"]
        bcup_rounds = session.query(BattlecupRound).filter(and_(BattlecupRound.battlecup == bcup.id,
                                                                BattlecupRound.round_ == bcup.current_round)).all()
        for bcup_round in bcup_rounds:
            if bcup_round.series_id == -1:
                session.query(BattlecupRound).filter(BattlecupRound.id == bcup_round.id).\
                    update({BattlecupRound.series_id: series_id})
        bcup_round_ids = [x.id for x in bcup_rounds]

        res = result.result_str
        winners = session.query(TeamHero.user). \
            filter(and_(TeamHero.hero_id == result.hero, TeamHero.league == league_id,
                        TeamHero.is_battlecup.is_(True))).all()
        for winner in winners:
            username = winner[0]
            userq = session.query(BattlecupUserRound).filter(and_(BattlecupUserRound.username == username,
                                                             BattlecupUserRound.battlecupround.in_(bcup_round_ids))).\
                order_by(BattlecupUserRound.id).first()  # is this really hacky? basically we get all battlecup rounds. then just assume should be updating last

            hero_count = session.query(func.count(TeamHero)).filter(and_(TeamHero.league == league_id,
                                                                         TeamHero.is_battlecup.is_(True),
                                                                         TeamHero.user == username)).scalar()
            if userq:
                add_result_to_user(userq, res, hero_count)
            # This isn't ideal. should rewrite function so can handle this
            else:
                bc_round_id = session.query(BattlecupRound.id).filter(or_(BattlecupRound.player_one == username,
                                                                      BattlecupRound.player_two == username)).\
                                                                      filter(BattlecupRound.id.in_(bcup_round_ids)
                                                                      ).first()[0]
                picks = 1 if "p" in res else 0
                wins = 1 if "w" in res else 0
                bans = 1 if "b" in res else 0
                points = (0.5 ** (5 - hero_count)) * Result.result_to_value(res)
                session.add(BattlecupUserRound(bc_round_id, username, points, picks, bans, wins))
                print "Battlecup: addin %s points to %s" % (points, username)
        transaction.commit()


def declare_bcup_rounds_winners(session, bcup_round):
    with transaction.manager:
        p1, p2 = session.query(BattlecupUserRound).filter(BattlecupUserRound.battlecupround == bcup_round.id).all()
        if p1.points > p2.points:
            bcup_round.winner = 1
        elif p2.points > p1.points:
            bcup_round.winner = 2
        else:
            if p1.wins > p2.wins:
                bcup_round.winner = 1
                p1.points += 0.1
            elif p2.wins > p1.wins:
                bcup_round.winner = 2
                p2.points += 0.1
            else:
                if p1.picks > p2.picks:
                    p1.points += 0.1
                    bcup_round.winner = 1
                elif p2.picks > p1.picks:
                    bcup_round.winner = 2
                    p2.points += 0.1
                else:
                    if p1.bans > p2.bans:
                        p1.points += 0.1
                        bcup_round.winner = 1
                    elif p2.bans > p1.bans:
                        bcup_round.winner = 2
                        p2.points += 0.1
                    else:
                        winner = random.randint(1, 2)
                        if winner == 1:
                            p1.points += 0.1
                            bcup_round.winner = 1
                        else:
                            bcup_round.winner = 2
                            p2.points += 0.1
        transaction.commit()


def new_bcup_round(session, league_id, series_id, bcup, previous_round_1, previous_round_2, losers=False):
    print "Stuffz\n", previous_round_1.player_one, previous_round_1.player_two
    print "Stuffz\n", previous_round_2.player_one, previous_round_2.player_two
    print "hahah", previous_round_1.id, previous_round_2.id
    winner_1 = previous_round_1.player_one if previous_round_1.winner == 1 else previous_round_1.player_two
    winner_2 = previous_round_2.player_one if previous_round_2.winner == 1 else previous_round_2.player_two

    if losers:  # so winner_1 and _2 are really the losers!
        winner_1 = previous_round_1.player_one if previous_round_1.winner == 2 else previous_round_1.player_two
        winner_2 = previous_round_2.player_one if previous_round_2.winner == 1 else previous_round_2.player_two
    import pdb; pdb.set_trace()
    with transaction.manager:
        session.add(BattlecupRound(bcup.id, bcup.current_round, series_id, winner_1, winner_2))
        transaction.commit()

    new_id = session.query(func.max(BattlecupRound.id)).scalar()
    with transaction.manager:
        session.add(BattlecupUserRound(new_id, winner_1, 0, 0, 0, 0))
        session.add(BattlecupUserRound(new_id, winner_2, 0, 0, 0, 0))
        transaction.commit()
    return


def update_hero_values(session, league):
    # hmm. there seeem to be sooo many needless loop iterations in this code :(
    league_id = league.id
    bcups = []
    for bcup in session.query(Battlecup).filter(and_(Battlecup.league == league_id,
                                                     Battlecup.day == league.current_day)).all():
        bcup_rounds = session.query(BattlecupRound).filter(and_(BattlecupRound.battlecup == bcup.id,
                                                               BattlecupRound.round_ == bcup.current_round)).all()
        bcups.append({"bcup": bcup, "bcup_rounds": bcup_rounds})
        print bcups

    new_results = session.query(Result).filter(Result.applied.is_(False)).\
        filter(Result.tournament_id == league_id).all()

    for result in new_results:
        res = result.result_str
        heroq = session.query(Hero).filter(and_(Hero.id == result.hero,
                                                Hero.is_battlecup.is_(False),
                                                Hero.league == league_id)).first()
        if not heroq: # temp for no underlord
            continue  #TODO remove!!!
        print result.match_id
        print "Hero id: ", result.hero
        if "p" in res:
            heroq.picks += 1
        if "w" in res:
            heroq.wins += 1
        if "b" in res:
            heroq.bans += 1
        print "Would add %s to hero points", Result.result_to_value(res)
        heroq.points += Result.result_to_value(res)

        result.applied = True

        # move this up to top. use queries already there
        series_id = result.series_id

        # -1 for 1st series day
        other_series_count = session.query(func.count(BattlecupRound)).filter(
            and_(BattlecupRound.series_id != series_id, BattlecupRound.series_id != -1)).scalar()
        num_series = Battlecup.num_series_this_round(bcups[0]["bcup"].current_round,
                                                     bcups[0]["bcup"].series_per_round)

        if other_series_count > 0 and other_series_count + 1 >= num_series:
            print "DOING NEW CUP"
            for bcup in bcups:  # move this loop up
                #bcup["bcup"].current_round += 1
                num_games_in_round = len(bcup["bcup_rounds"])
                if num_games_in_round > 1:
                    for i, bcup_round in enumerate(session.query(BattlecupRound).filter(and_(BattlecupRound.battlecup == bcup["bcup"].id,
                                                               BattlecupRound.round_ == bcup["bcup"].current_round)).all()):
                        declare_bcup_rounds_winners(session, bcup_round)
                        if i % 2 != 0:
                                if num_games_in_round == 2:  # add 3rd place playoff
                                    new_bcup_round(session, league_id, series_id, bcup["bcup"],
                                                   last_round, bcup_round, losers=True)
                                new_bcup_round(session, league_id, series_id, bcup["bcup"],
                                               last_round, bcup_round)
                        else:
                            last_round = bcup_round
                update_battlecup_points(session, result, series_id, bcup, league_id)  # refactor this. dont call 2
                bcup["bcup"].current_round += 1
        else:
            print "OLD CUP"
            for bcup in bcups:
                update_battlecup_points(session, result, series_id, bcup, league_id)
        with transaction.manager:
            update_league_points(session, result, league_id)  # update total league
            update_league_points(session, result, league_id, day=league.current_day)  # update current day
            transaction.commit()

    with transaction.manager:
        set_user_rankings(session, league_id)
        set_user_rankings(session, league_id, day=league.current_day)

        transaction.commit()


def main():
    session = make_session()
    for league in session.query(League).all():
        if league.id == 4979:
            update_hero_values(session, league)

if __name__ == "__main__":
    main()
