from operator import and_



import transaction
from fantasydota.lib.session_utils import make_session
from fantasydota.models import TeamHero, User, Hero, Result
from fantasydota.util.random_function import bprint


def main():
    '''
    Fix user money to what it should be based on heroes in their team
    remove hero if team over max value
    :return:
    '''
    session = make_session()

    offset = [["esricgodbear", 3, 5],
    ["kaleb200", 4, 5],
    ["hockstein", 3, 5],
    ["dadostar97", 4, 5],
    ["badeetzmaru", 4, 5],
    ["mattspaul", -2, 5],
    ["johnnyisacockmuncher", 2, 5]]
    with transaction.manager:
        #users = session.query(User).all()
        for off in offset:
            user = session.query(User).filter(User.username == off[0]).first()
            #heroes = session.query(TeamHero).filter(and_(TeamHero.user == user.username, TeamHero.active == True)).all()
            results = session.query(Result).filter(Result.match_id == 2836078773).all()
            for res in results:
                user.points += (0.5 ** (5 - off[2])) * Result.result_to_value(res.win)
                user.points -= (0.5 ** (5 - off[1])) * Result.result_to_value(res.win)
                bcp = session.query(BattlecupUserPoints).filter(BattlecupUserPoints.username == off[0]).first()
                bcp.points += (0.5 ** (5 - off[2])) * Result.result_to_value(res.win)
                bcp.points -= (0.5 ** (5 - off[1])) * Result.result_to_value(res.win)


        #transaction.commit()

if __name__ == "__main__":
    main()
