from _socket import gethostname
import datetime
from passlib.handlers.bcrypt import bcrypt
from sqlalchemy import BigInteger
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Sequence,
    String,
    Date,
    func, Boolean,
    create_engine, UniqueConstraint, ForeignKey)
from sqlalchemy import Float
from sqlalchemy.orm import sessionmaker, scoped_session

from sqlalchemy.ext.declarative import declarative_base
from pyramid.security import (
    Allow,
    Everyone,
    Authenticated, ALL_PERMISSIONS)
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.pool import NullPool

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


class Base(object):
    def __json__(self, request):
        json_exclude = getattr(self, '__json_exclude__', set())
        j_dict = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_') and key not in json_exclude:  # Dont serialise private attrs and internal sqlalchemy attrs
                j_dict[key] = value
        return j_dict

Base = declarative_base(cls=Base)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, Sequence('id'), primary_key=True)
    username = Column('username', String(50), unique=True, nullable=False, index=True)
    password = Column('password', String(300), nullable=False)
    email = Column('email', String(300))
    registered_on = Column('registered_on', Date, default=func.now())
    last_logged_in = Column('last_login', Date, default=func.now())

    def __init__(self, username, password, email=""):
        self.username = username
        self.password = bcrypt.encrypt(password)
        self.email = email

    def validate_password(self, password):
        return bcrypt.verify(password, self.password)


class League(Base):
    __tablename__ = "league"
    id = Column(Integer, primary_key=True)  # use id that matches dota2 api
    name = Column('name', String(100), nullable=False)
    status = Column('status', Integer, default=0)  # 0 not started. 1 is running. 2 is ended
    transfer_open = Column(Boolean, default=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name
    

class UserLeague(Base):
    __tablename__ = "user_league"
    id = Column(Integer, Sequence('id'), primary_key=True)
    username = Column('username', String(50), ForeignKey(User.username), index=True, nullable=False)
    league = Column('league', Integer, ForeignKey(League.id), index=True)
    money = Column('money', Float, default=50.0)
    points = Column('points', Float, default=0.0)
    picks = Column('picks', Integer, default=0)
    bans = Column('bans', Integer, default=0)
    wins = Column('wins', Integer, default=0)
    points_rank = Column('points_rank', Integer, default="None")
    wins_rank = Column('wins_rank', Integer, default="None")
    picks_rank = Column('picks_rank', Integer, default="None")
    bans_rank = Column('bans_rank', Integer, default="None")

    def __init__(self, username, league):
        self.username = username
        self.league = league


# check if I should use polymorphic mapping for this with userLeague
class UserLeagueDay(UserLeague):
    __tablename__ = "user_league_day"
    user_league = Column(Integer, ForeignKey(UserLeague.id), index=True)
    day = Column('day', Integer, index=True)
    stage = Column('stage', Integer)  # 0 qualifiers, 1 group stage, 2 main event
    
    def __init__(self, user_league, day, stage, *args, **kwargs):
        super(UserLeagueDay, self).__init__(*args, **kwargs)
        self.user_league = user_league
        self.day = day
        self.stage = stage


#class HistoryUser(Base):
#    __tablename__ = "history_user"
#    id = Column(Integer, Sequence('id'), primary_key=True)
#    username = Column('username', String(50), nullable=False)
#    date = Column('last_login', Date, default=func.now())  # hmm how can I fix this typo.without break stuff?
#
#    money = Column('money', Float)
#    points = Column('points', Integer)
#    picks = Column('picks', Integer)
#    bans = Column('bans', Integer)
#    wins = Column('wins', Integer)
#    hero_one = Column('hero_one', Integer)
#    hero_two = Column('hero_two', Integer)
#    hero_three = Column('hero_three', Integer)
#    hero_four = Column('hero_four', Integer)
#    hero_five = Column('hero_five', Integer)
#
#    def __init__(self, username, money, points, picks, bans, wins, h1, h2, h3, h4, h5):
#        self.username = username
#        self.money = money
#        self.points = points
#        self.picks = picks
#        self.bans = bans
#        self.wins = wins
#        self.hero_one = h1
#        self.hero_two = h2
#        self.hero_three = h3
#        self.hero_four = h4
#        self.hero_five = h5
#

class Battlecup(Base):
    __tablename__ = "battlecup"
    id = Column(Integer, Sequence('id'), primary_key=True)
    league = Column('league', Integer, ForeignKey(League.id), index=True)
    day = Column('day', Integer, index=True)
    total_rounds = Column(Integer)
    last_completed_round = Column(Integer, default=0)
    transfer_open = Column(Boolean, default=True)

    def __init__(self, league, day, total_rounds):
        self.league = league
        self.total_rounds = total_rounds
        self.day = day

class BattlecupUser(Base):
    __tablename__ = "battlecup_user"
    id = Column(Integer, Sequence('id'), primary_key=True)
    battlecup = Column('battlecup', Integer, ForeignKey(Battlecup.id), index=True) # should index be here?
    username = Column('username', String(50), ForeignKey(User.username), index=True, nullable=False)
    #user_id = Column('user_id', Integer, ForeignKey(User.user_id), index=True)  # should index be here?
    round_out = Column('round_out', Integer)

    def __init__(self, battlecup, username):
        self.battlecup = battlecup
        self.username = username

class BattlecupRound(Base):
    __tablename__ = "battlecup_round"
    id = Column(Integer, Sequence('id'), primary_key=True)
    battlecup = Column('battlecup', Integer, ForeignKey(BattlecupUser.id), index=True)
    round_ = Column(Integer, index=True)
    series_id = Column('series_id', BigInteger)
    
    def __init__(self, battlecup, round_, series_id):
        self.battlecup = battlecup
        self.round_ = round_
        self.series_id = series_id

class BattlecupUserRound(Base):
    __tablename__ = "battlecup_user_points"
    id = Column(Integer, Sequence('id'), primary_key=True)
    battlecupround = Column('battlecupround', Integer, ForeignKey(BattlecupRound.id), index=True)
    points = Column('points', Float)
    picks = Column('picks', Integer, default=0)
    bans = Column('bans', Integer, default=0)
    wins = Column('wins', Integer, default=0)

    def __init__(self, battlecupround, points, picks, bans, wins):
        self.battlecupround = battlecupround
        self.points = points
        self.picks = picks
        self.bans = bans
        self.wins = wins


# class UserRank(Base):
#     __tablename__ = "user_rank"
#     user = Column('user', String(50), ForeignKey(User.username), unique=True, nullable=False, primary_key=True)
#     points_rank = Column('points_rank', Integer, default="None")
#     wins_rank = Column('wins_rank', Integer, default="None")
#     picks_rank = Column('picks_rank', Integer, default="None")
#     bans_rank = Column('bans_rank', Integer, default="None")
#
#     def __init__(self, user):
#         self.user = user


class Friend(Base):
    __tablename__ = "friend"
    id = Column(Integer, Sequence('id'), primary_key=True)
    user = Column('user', String(50), ForeignKey(User.username), nullable=False)
    friend = Column('friend', String(50), ForeignKey(User.username), nullable=False)

    def __init__(self, user, friend):
        self.user = user
        self.friend = friend
    # Is some fucking fuckhead going to break this by adding themselves as a friend?
        # should also make user/friend be a unique pair. so cant friend twice


class Hero(Base):
    __tablename__ = "hero"
    id = Column('id', Integer, primary_key=True)  # api hero ids start at 1
    name = Column('name', String(100), unique=True, nullable=False)  #index=true?

    def __init__(self, id, name):
        self.id = id
        self.name = name


class HeroLeague(Base):
    __tablename__ = "hero_league"
    id = Column(Integer, Sequence('id'), primary_key=True)
    hero = Column('hero', Integer, ForeignKey(Hero.id), index=True)  # api hero ids start at 1
    #name = Column('name', String(100), ForeignKey(Hero.name), index=True)  #index=true?
    league = Column(Integer, ForeignKey(League.id), index=True)
    value = Column('value', Float, default=10.0)
    points = Column('points', Integer, default=0)
    picks = Column('picks', Integer, default=0)
    bans = Column('bans', Integer, default=0)
    wins = Column('wins', Integer, default=0)
    active = Column(Boolean, default=True)  # this is for when valve release patch midway through tournament and add/remove from cm

    def __init__(self, hero, value, league):
        self.hero = hero
        self.value = value
        self.league = league


class HeroBattlecup(Base):
    __tablename__ = "hero_battlecup"
    id = Column(Integer, Sequence('id'), primary_key=True)
    hero = Column('hero', Integer, ForeignKey(Hero.id), index=True)  # api hero ids start at 1
    name = Column('name', String(100), ForeignKey(Hero.name), index=True) 
    battlecup = Column(Integer, ForeignKey(Battlecup.id), index=True)
    value = Column('value', Float, default=10.0)
    points = Column('points', Integer, default=0)
    picks = Column('picks', Integer, default=0)
    bans = Column('bans', Integer, default=0)
    wins = Column('wins', Integer, default=0)
    active = Column(Boolean, default=True)

    def __init__(self, hero, name, value, battlecup):
        self.hero = hero
        self.name = name
        self.value = value
        self.battlecup = battlecup


class TeamHeroLeague(Base):
    __tablename__ = "team_hero_league"
    id = Column(Integer, Sequence('id'), primary_key=True)
    user = Column('user', String(50), ForeignKey(User.username), index=True)
    hero = Column('hero', Integer, ForeignKey(Hero.id))
    league = Column(Integer, ForeignKey(League.id), index=True)
    active = Column('active', Boolean)
    to_trade = Column('to_trade', Boolean)

    def __init__(self, user, hero, league, active, to_trade):
        self.user = user
        self.hero = hero
        self.league = league
        self.active = active
        self.to_trade = to_trade


class TeamHeroBattlecup(Base):
    __tablename__ = "team_hero_battlecup"
    id = Column(Integer, Sequence('id'), primary_key=True)
    user = Column(String(50), ForeignKey(User.username), index=True)
    hero = Column(Integer, ForeignKey(Hero.id), index=True)
    battlecup = Column(Integer, ForeignKey(Battlecup.id), index=True)

    def __init__(self, user, hero, battlecup):
        self.user = user
        self.hero = hero
        self.battlecup = battlecup


# class Sale(Base):
#     __tablename__ = "sale"
#     sale_id = Column(Integer, Sequence('sale_id'), primary_key=True)
#     user = Column('user', String(50), ForeignKey('user.username'), nullable=False) # index true?
#     hero = Column('hero', Integer, ForeignKey('hero.hero_id'), nullable=False, index=True)
#     date = Column('date', Date, nullable=False, default=func.now())
#     number = Column('number', Integer, nullable=False)
#
#     def __init__(self, user, hero, number):
#         self.user = user
#         self.hero = hero
#         self.number = number


class Result(Base):
    __tablename__ = "result"
    id = Column(Integer, Sequence('id'), primary_key=True)
    match_id = Column('match_id', BigInteger, nullable=False, index=True)
    tournament_id = Column('tournament_id', Integer, nullable=False)
    hero = Column('hero', Integer, nullable=False)
    result_str = Column('result_str', String(20), nullable=False)
    timestamp = Column(Integer)
    applied = Column('applied', Boolean, default=False)
    series_id = Column('series_id', BigInteger)

    def __init__(self, tournament, hero, match, result_str, timestamp, series_id):
        self.tournament_id = tournament
        self.hero = hero
        self.match_id = match
        self.result_str = result_str
        self.timestamp = timestamp
        self.series_id = series_id

    @staticmethod
    def result_to_value(result_str):
        points_dict = {
            "b1": 2,
            "b2": 3,
            "b3": 4,
            "p1l": -2,
            "p2l": -1,
            "p3l": 0,
            "p1w": 10,
            "p2w": 12,
            "p3w": 14,
        }
        return points_dict[result_str]
