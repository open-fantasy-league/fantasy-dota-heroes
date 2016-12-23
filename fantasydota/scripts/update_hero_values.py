import transaction
from sqlalchemy import and_
from sqlalchemy import desc
from fantasydota.lib.session_utils import make_session
from fantasydota.models import Hero, Result, TeamHero, User, BattlecupUser, BattlecupUserPoints, Battlecup
from sqlalchemy import func


def set_user_rankings(session):
    # But is there a better way??
    wins_ranking = session.query(User.username).order_by(desc(User.wins)).all()
    for i, user in enumerate(wins_ranking):
        session.query(User).filter(User.username == user.username).\
            update({User.wins_rank: i+1})

    points_ranking = session.query(User.username).order_by(desc(User.points)).all()
    for i, user in enumerate(points_ranking):
        session.query(User).filter(User.username == user.username). \
            update({User.points_rank: i + 1})

    picks_ranking = session.query(User.username).order_by(desc(User.picks)).all()
    for i, user in enumerate(picks_ranking):
        session.query(User).filter(User.username == user.username). \
            update({User.picks_rank: i + 1})

    bans_ranking = session.query(User.username).order_by(desc(User.bans)).all()
    for i, user in enumerate(bans_ranking):
        session.query(User).filter(User.username == user.username)  . \
            update({User.bans_rank: i + 1})
    return


def update_hero_values(session):
    with transaction.manager:
        new_results = session.query(Result).filter(Result.applied.is_(False)).all()

        for result in new_results:
            res = result.result_str
            heroq = session.query(Hero).filter(Hero.hero_id == result.hero).first()
            '''
            if "p" in res:
                heroq.picks += 1
            if "w" in res:
                heroq.wins += 1
            if "b" in res:
                heroq.bans += 1
            print "Would add %s to hero points", Result.result_to_value(res)
            heroq.points += Result.result_to_value(res)
            '''

            # TODO put this into loop below
            users_who_won = session.query(TeamHero.user).\
                filter(and_(TeamHero.hero == result.hero, TeamHero.active == True)).all()
            for user_res in users_who_won:
                userq = session.query(User).filter(User.username == user_res[0]).first()
                hero_count = session.query(func.count(TeamHero)).filter(TeamHero.active == True).\
                    filter(TeamHero.user == userq.user_id)
                if "p" in res:
                    userq.picks += 1
                if "w" in res:
                    userq.wins += 1
                if "b" in res:
                    userq.bans += 1
                to_add = (0.5 ** (5 - hero_count)) * Result.result_to_value(res)
                print "addin %s points to %s" % (to_add, user_res[0])
                userq.points += to_add
            result.applied = True


            series_id = result.series_id
            if not session.query(BattlecupUserPoints).filter(BattlecupUserPoints.series_id == series_id).first():
                session.query(Battlecup).update({Battlecup.last_completed_round: Battlecup.last_completed_round + 1})

            for user_ in session.query(User).all():
                username = user_.username
                # new series. so old series has finished
                hero_count = session.query(func.count(TeamHero)).filter(TeamHero.active == True). \
                    filter(TeamHero.user == user_.user_id)

                has_hero = session.query(TeamHero).filter(TeamHero.user == user_.username). \
                    filter(and_(TeamHero.hero == result.hero, TeamHero.active == True)).first()
                battlecup_id = session.query(BattlecupUser.battlecup_id).\
                    filter(BattlecupUser.username == user_.username).first()
                if not battlecup_id:
                    print "battlecup user doesnt exist"
                    continue
                else:
                    battlecup_id = battlecup_id[0]
                bcq = session.query(BattlecupUserPoints).filter(and_(BattlecupUserPoints.username == username,
                                                                     BattlecupUserPoints.series_id == series_id)).first()
                if not bcq:
                    bcq = BattlecupUserPoints(battlecup_id, username, user_.user_id,
                                              result.date,
                                              result.series_id, 0, 0, 0)
                    session.add(bcq)
                if has_hero:
                    print "would update bcq"
                    bcq.points += (0.5 ** (5 - hero_count)) * Result.result_to_value(res)

        set_user_rankings(session)

        transaction.commit()


def main():
    session = make_session()
    update_hero_values(session)

if __name__ == "__main__":
    main()
