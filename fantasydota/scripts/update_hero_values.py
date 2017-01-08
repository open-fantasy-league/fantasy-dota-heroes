import random

import transaction
from fantasydota.lib.battlecup import FakePlayer
from fantasydota.lib.session_utils import make_session
from fantasydota.models import Hero, Result, Battlecup, LeagueUser, League, LeagueUserDay, \
    BattlecupUserRound, BattlecupRound, TeamHero
from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import func


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


def update_battlecup_points(session, result, series_id, bcup, league_id):
    bcup_rounds = session.query(BattlecupRound).filter(and_(BattlecupRound.battlecup == bcup.id,
                                                            BattlecupRound.round_ == bcup.current_round)).all()
    for bcup_round in bcup_rounds:
        if bcup_round.series_id == -1:
            session.query(BattlecupRound).filter(BattlecupRound.id == bcup_round.id).\
                update({BattlecupRound.series_id: series_id})
    bcup_round_ids = [x.id for x in bcup_rounds]
    for player in session.query(BattlecupUserRound).filter(BattlecupUserRound.battlecupround.in_(bcup_round_ids)).all():
        winner = session.query(TeamHero.user). \
            filter(and_(TeamHero.hero_id == result.hero, TeamHero.league == league_id,
                        TeamHero.user == player.username,
                        TeamHero.is_battlecup.is_(True))).first()

        if winner:
            hero_count = session.query(func.count(TeamHero)).filter(and_(TeamHero.league == league_id,
                                                                         TeamHero.is_battlecup.is_(True),
                                                                         TeamHero.user == player.username)).scalar()
            add_result_to_user(player, result.result_str, hero_count)


def declare_bcup_rounds_winners(session, bcup_round):
    bur_q = session.query(BattlecupUserRound).filter(BattlecupUserRound.battlecupround == bcup_round.id)
    res = bur_q.order_by(BattlecupUserRound.id).all()
    p1 = res[0]
    try:
        p2 = res[1]
    except IndexError:
        p2 = FakePlayer()# bye
    print "usr: %s, points: %s" % (p1.username, p1.points)
    print "usr: %s, points: %s" % (p2.username, p2.points)
    if p1.points > p2.points:
        session.query(BattlecupRound).\
            filter(BattlecupRound.id == bcup_round.id).update({BattlecupRound.winner: 1})
        return 1
    elif p2.points > p1.points:
        session.query(BattlecupRound). \
            filter(BattlecupRound.id == bcup_round.id).update({BattlecupRound.winner: 2})
        return 2
    else:
        if p1.wins > p2.wins:
            session.query(BattlecupRound). \
                filter(BattlecupRound.id == bcup_round.id).update({BattlecupRound.winner: 1})
            bur_q.filter(BattlecupUserRound.username == p1.username).\
                update({BattlecupUserRound.points: BattlecupUserRound.points + 0.1})
            return 1
        elif p2.wins > p1.wins:
            session.query(BattlecupRound). \
                filter(BattlecupRound.id == bcup_round.id).update({BattlecupRound.winner: 2})
            bur_q.filter(BattlecupUserRound.username == p2.username).\
                update({BattlecupUserRound.points: BattlecupUserRound.points + 0.1})
            return 2
        else:
            if p1.picks > p2.picks:
                session.query(BattlecupRound). \
                    filter(BattlecupRound.id == bcup_round.id).update({BattlecupRound.winner: 1})
                bur_q.filter(BattlecupUserRound.username == p1.username). \
                    update({BattlecupUserRound.points: BattlecupUserRound.points + 0.1})
                return 1
            elif p2.picks > p1.picks:
                session.query(BattlecupRound). \
                    filter(BattlecupRound.id == bcup_round.id).update({BattlecupRound.winner: 2})
                bur_q.filter(BattlecupUserRound.username == p2.username). \
                    update({BattlecupUserRound.points: BattlecupUserRound.points + 0.1})
                return 2
            else:
                if p1.bans > p2.bans:
                    session.query(BattlecupRound). \
                        filter(BattlecupRound.id == bcup_round.id).update({BattlecupRound.winner: 1})
                    bur_q.filter(BattlecupUserRound.username == p1.username). \
                        update({BattlecupUserRound.points: BattlecupUserRound.points + 0.1})
                    return 1
                elif p2.bans > p1.bans:
                    session.query(BattlecupRound). \
                        filter(BattlecupRound.id == bcup_round.id).update({BattlecupRound.winner: 2})
                    bur_q.filter(BattlecupUserRound.username == p2.username). \
                        update({BattlecupUserRound.points: BattlecupUserRound.points + 0.1})
                    return 2
                else:
                    winner = random.randint(1, 2)
                    if winner == 1:
                        session.query(BattlecupRound). \
                            filter(BattlecupRound.id == bcup_round.id).update({BattlecupRound.winner: 1})
                        bur_q.filter(BattlecupUserRound.username == p1.username). \
                            update({BattlecupUserRound.points: BattlecupUserRound.points + 0.1})
                        return 1
                    else:
                        session.query(BattlecupRound). \
                            filter(BattlecupRound.id == bcup_round.id).update({BattlecupRound.winner: 2})
                        bur_q.filter(BattlecupUserRound.username == p2.username). \
                            update({BattlecupUserRound.points: BattlecupUserRound.points + 0.1})
                        return 2


def new_bcup_round(session, league_id, series_id, bcup, previous_round_1, previous_round_2, previous_1_winner,
                   previous_2_winner, losers=False):
    winner_1 = previous_round_1.player_one if previous_1_winner == 1 else previous_round_1.player_two
    winner_2 = previous_round_2.player_one if previous_2_winner == 1 else previous_round_2.player_two

    if losers:  # so winner_1 and _2 are really the losers!
        winner_1 = previous_round_1.player_one if previous_1_winner == 2 else previous_round_1.player_two
        winner_2 = previous_round_2.player_one if previous_2_winner == 2 else previous_round_2.player_two
    session.add(BattlecupRound(bcup.id, bcup.current_round + 1, series_id, winner_1, winner_2))

    new_id = session.query(func.max(BattlecupRound.id)).scalar()
    session.add(BattlecupUserRound(new_id, winner_1, 0, 0, 0, 0))
    session.add(BattlecupUserRound(new_id, winner_2, 0, 0, 0, 0))
        
    return


def update_hero_values(session, league):
    league_id = league.id
    new_results = session.query(Result).filter(Result.applied.is_(False)).\
        filter(Result.tournament_id == league_id).all()

    for i, result in enumerate(new_results):
        res = result.result_str
        with transaction.manager:
            # More than one because we have battlecup and league
            heroq_all = session.query(Hero).filter(and_(Hero.id == result.hero,
                                                    Hero.league == league_id)).all()
            if not heroq_all:  # temp for no underlord
                continue  # TODO remove!!!
            for heroq in heroq_all:
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

            transaction.commit()
	
        # move this up to top. use queries already there
        series_id = result.series_id

        bcups = session.query(Battlecup).filter(and_(Battlecup.league == league_id,
                                                     Battlecup.day == league.current_day)).all()
        for bcup in bcups:
            # -1 for 1st series day
            other_series_count = session.query(BattlecupRound).filter(
                and_(BattlecupRound.series_id != series_id, BattlecupRound.round_ == bcup.current_round,
                     BattlecupRound.series_id != -1)).group_by(BattlecupRound.series_id).all() or []
	    other_series_count = len(other_series_count)
	    #other_series_count = 2  # should replace 0's with timestamp. have to hack now
	    print "other_ser_cout", other_series_count

            try:
                num_series = Battlecup.num_series_this_round(bcup.current_round,
                                                bcup.series_per_round)
                do_new_cup = other_series_count > 0 and other_series_count >= num_series
            except:  # we are in the finals. no new cups
                do_new_cup = False
	    do_new_cup = True if i == 0 else False
            if do_new_cup:
                print "DOING NEW CUP"
                bcup_rounds = session.query(BattlecupRound).\
                    filter(and_(BattlecupRound.battlecup == bcup.id, BattlecupRound.round_ == bcup.current_round)).order_by(BattlecupRound.id).all()
                num_games_in_round = len(bcup_rounds)
                if num_games_in_round > 1:
                    for i, bcup_round in enumerate(bcup_rounds):
                        with transaction.manager:
                            # This function has side-effect of updating winner field
                            # im not sure why the separate transactions mean winner hasnt updated by new_bcup_round
                            round_winner = declare_bcup_rounds_winners(session, bcup_round)
			    print "winner: ", round_winner
                            transaction.commit()
                        with transaction.manager:
                            if i % 2 != 0:
                                if num_games_in_round == 2:  # add 3rd place playoff
                                    new_bcup_round(session, league_id, series_id, bcup,
                                                   last_round, bcup_round, last_round_winner, round_winner,
                                                   losers=True)
                                new_bcup_round(session, league_id, series_id, bcup,
                                               last_round, bcup_round, last_round_winner, round_winner)
                            else:
                                last_round = bcup_round
                                last_round_winner = round_winner
                            transaction.commit()
                with transaction.manager:
		    session.query(Battlecup).filter(Battlecup.id == bcup.id).\
                        update({Battlecup.current_round: Battlecup.current_round + 1})
                    update_battlecup_points(session, result, series_id, bcup, league_id)  # refactor this. dont call 2
                    #session.query(Battlecup).filter(Battlecup.id == bcup.id).\
                    #    update({Battlecup.current_round: Battlecup.current_round + 1})
                    transaction.commit()

            else:
                with transaction.manager:
                    update_battlecup_points(session, result, series_id, bcup, league_id)
                    transaction.commit()
	
	with transaction.manager:
            update_league_points(session, result, league_id)  # update total league
            update_league_points(session, result, league_id, day=league.current_day)  # update current day
            session.query(Result).filter(Result.id == result.id).update({Result.applied: True})
            transaction.commit()
	
    with transaction.manager:
        set_user_rankings(session, league_id)
        set_user_rankings(session, league_id, day=league.current_day)
        transaction.commit()


def main():
    session = make_session()
    for league in session.query(League).all():
        update_hero_values(session, league)

if __name__ == "__main__":
    main()
