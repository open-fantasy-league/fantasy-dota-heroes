# import transaction
# from sqlalchemy import and_
# from sqlalchemy.sql import func
# from fantasydota.lib.session_utils import make_session
# from fantasydota.models import TeamHeroLeague, User
#
#
# def main():
#     session = make_session()
#     with transaction.manager:
#         users = session.query(User).all()
#         for user in users:
#             team = session.query(TeamHero.hero).filter(and_(TeamHero.user == user.username, TeamHero.active == True)).all()
#             team2 = []
#
#             for i in range(5):
#                 if i + 1 <= len(team):
#                     team2.append(team[i][0])
#                 else:
#                     team2.append(0)
#             h1, h2, h3, h4, h5 = team2
#             last_history = session.query(HistoryUser).filter(and_(HistoryUser.username == user.username,
#                                                                   HistoryUser.date != func.now())).all()
#             print "last hist", last_history
#             today_points, today_picks, today_bans, today_wins = user.points, user.picks, user.bans, user.wins
#             for hist in last_history:
#                 today_points -= hist.points
#                 today_picks -= hist.picks
#                 today_bans -= hist.bans
#                 today_wins -= hist.wins
#             new_history = HistoryUser(user.username, user.money, today_points, today_picks, today_bans, today_wins,
#                                       h1, h2, h3, h4, h5)
#             session.add(new_history)
#
#         transaction.commit()
#
# if __name__ == "__main__":
#     main()


# deperecated?