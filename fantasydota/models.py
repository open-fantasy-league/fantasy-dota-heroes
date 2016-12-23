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


class Root(object):
    __acl__ = [ (Allow, Authenticated, 'create'),
                (Allow, 'group:editor', 'edit'),
                (Allow, 'g:admin', ALL_PERMISSIONS)]

    def __init__(self, request):
        self.request = request


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
    user_id = Column(Integer, Sequence('user_id'), primary_key=True)
    username = Column('username', String(50), unique=True, nullable=False)
    password = Column('password', String(300), nullable=False)
    email = Column('email', String(300))
    registered_on = Column('registered_on', Date, default=func.now())
    last_logged_in = Column('last_login', Date, default=func.now())
    money = Column('money', Float, default=50.0)
    points = Column('points', Integer, default=0)
    picks = Column('picks', Integer, default=0)
    bans = Column('bans', Integer, default=0)
    wins = Column('wins', Integer, default=0)
    points_rank = Column('points_rank', Integer, default="None")
    wins_rank = Column('wins_rank', Integer, default="None")
    picks_rank = Column('picks_rank', Integer, default="None")
    bans_rank = Column('bans_rank', Integer, default="None")
    hero_count = Column('hero_count', Integer, default=0)

    def __init__(self, username, password, email=""):
        self.username = username
        self.password = bcrypt.encrypt(password)
        self.email = email

    def validate_password(self, password):
        return bcrypt.verify(password, self.password)


class HistoryUser(Base):
    __tablename__ = "history_user"
    id = Column(Integer, Sequence('id'), primary_key=True)
    username = Column('username', String(50), nullable=False)
    date = Column('last_login', Date, default=func.now())  # hmm how can I fix this typo.without break stuff?

    money = Column('money', Float)
    points = Column('points', Integer)
    picks = Column('picks', Integer)
    bans = Column('bans', Integer)
    wins = Column('wins', Integer)
    hero_one = Column('hero_one', Integer)
    hero_two = Column('hero_two', Integer)
    hero_three = Column('hero_three', Integer)
    hero_four = Column('hero_four', Integer)
    hero_five = Column('hero_five', Integer)

    def __init__(self, username, money, points, picks, bans, wins, h1, h2, h3, h4, h5):
        self.username = username
        self.money = money
        self.points = points
        self.picks = picks
        self.bans = bans
        self.wins = wins
        self.hero_one = h1
        self.hero_two = h2
        self.hero_three = h3
        self.hero_four = h4
        self.hero_five = h5


class Battlecup(Base):
    __tablename__ = "battlecup"
    id = Column(Integer, Sequence('id'), primary_key=True)
    total_rounds = Column(Integer)
    last_completed_round = Column(Integer)

    def __init__(self, total_rounds, last_completed_round):
        self.total_rounds = total_rounds
        self.last_completed_round = last_completed_round


class BattlecupUser(Base):
    __tablename__ = "battlecup_user"
    id = Column(Integer, Sequence('id'), primary_key=True)
    battlecup_id = Column('battlecup_id', Integer, ForeignKey(Battlecup.id), index=True) # should index be here?
    username = Column('username', String(50), ForeignKey(User.username), nullable=False)
    user_id = Column('user_id', Integer, ForeignKey(User.user_id), index=True)  # should index be here?
    round_out = Column('round_out', Integer, default=0)

    def __init__(self, battlecup_id, username, user_id):
        self.battlecup_id = battlecup_id
        self.username = username
        self.user_id = user_id


class BattlecupUserPoints(Base):
    __tablename__ = "battlecup_user_points"
    id = Column(Integer, Sequence('id'), primary_key=True)
    battlecup_id = Column('battlecup_id', Integer, ForeignKey(Battlecup.id), index=True) # should index be here?
    username = Column('username', String(50), ForeignKey(User.username), nullable=False, index=True)
    user_id = Column('user_id', Integer, ForeignKey(User.user_id))  # should index be here?
    date = Column('date', Integer)
    series_id = Column('series_id', BigInteger)
    points = Column('points', Integer)
    ser_round = Column('ser_round', Integer)
    round_out = Column('round_out', Integer)

    def __init__(self, battlecup_id, username, user_id, date, series_id, points, ser_round, round_out):
        self.battlecup_id = battlecup_id
        self.username = username
        self.user_id = user_id
        self.date = date
        self.series_id = series_id
        self.points = points
        self.ser_round = ser_round
        self.round_out = round_out


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
    friend_id = Column(Integer, Sequence('friend_id'), primary_key=True)
    user = Column('user', String(50), ForeignKey(User.username), nullable=False)
    friend = Column('friend', String(50), ForeignKey(User.username), nullable=False)

    def __init__(self, user, friend):
        self.user = user
        self.friend = friend
    # Is some fucking fuckhead going to break this by adding themselves as a friend?
        # should also make user/friend be a unique pair. so cant friend twice


class Hero(Base):
    __tablename__ = "hero"
    hero_id = Column('hero_id', Integer, primary_key=True)  # api hero ids start at 1
    name = Column('name', String(100), unique=True, nullable=False)  #index=true?
    value = Column('value', Float, default=10.0)
    points = Column('points', Integer, default=0)
    picks = Column('picks', Integer, default=0)
    bans = Column('bans', Integer, default=0)
    wins = Column('wins', Integer, default=0)

    def __init__(self, id, name, value):
        self.hero_id = id
        self.name = name
        self.value = value


class TeamHero(Base):
    __tablename__ = "team_hero"
    team_hero_id = Column(Integer, Sequence('team_hero_id'), primary_key=True)
    user = Column('user', String(50), ForeignKey(User.username), index=True)
    hero = Column('hero', Integer, ForeignKey(Hero.hero_id))
    active = Column('active', Boolean)
    to_trade = Column('to_trade', Boolean)

    def __init__(self, user, hero, active, to_trade):
        self.user = user
        self.hero = hero
        self.active = active
        self.to_trade = to_trade

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
    result_id = Column(Integer, Sequence('result_id'), primary_key=True)
    match_id = Column('match_id', BigInteger, nullable=False)
    tournament_id = Column('tournament_id', Integer, nullable=False)
    hero = Column('hero', Integer, nullable=False)
    result_str = Column('result_str', String(20), nullable=False)
    date = Column('date', Integer)
    applied = Column('applied', Boolean, default=False)
    series_id = Column('series_id', BigInteger)

    def __init__(self, tournament, hero, match, result_str, date, series_id):
        self.tournament_id = tournament
        self.hero = hero
        self.match_id = match
        self.result_str = result_str
        self.date = date
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
