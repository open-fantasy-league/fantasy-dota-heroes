import datetime
from passlib.handlers.bcrypt import bcrypt
from sqlalchemy import BigInteger
from sqlalchemy import (
    Column,
    Integer,
    Sequence,
    String,
    Date,
    func, Boolean,
    ForeignKey)
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import ZopeTransactionExtension
import time

from fantasydota.lib.herolist import heroes

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
    username = Column(String(20), nullable=False, index=True)
    password = Column(String(300), nullable=False)
    email = Column(String(300))
    registered_on = Column(Date, default=func.now())
    last_login = Column(Date, default=func.now())
    contactable = Column(Boolean, default=False)
    autofill_team = Column(Boolean, default=False)
    daily_wins = Column(Integer, default=0)
    # TODO is_steam = Column(Boolean, default=True) # set False when called. add to below init

    def __init__(self, username, password="", email=""):
        self.username = username
        self.password = bcrypt.encrypt(password)
        self.email = email

    def validate_password(self, password):
        return bcrypt.verify(password, self.password)


class PasswordReset(Base):
    __tablename__ = "password_reset"
    id = Column(Integer, Sequence('id'), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    guid = Column(String(300), nullable=False)
    time = Column(DateTime, default=func.now())
    ip = Column(String(30))  # This is so can ip block anyone who spam resets passwords for someone
    counter = Column(Integer, default=0)  # Don't let people get spammed

    def __init__(self, user_id, guid, ip):
        self.user_id = user_id
        self.guid = guid
        self.ip = ip

    def validate_guid(self, guid):
        return bcrypt.verify(str(self.user_id), guid)


class League(Base):
    __tablename__ = "league"
    id = Column(Integer, primary_key=True)  # use id that matches dota2 api
    name = Column(String(100), nullable=False)
    status = Column(Integer, default=0)  # 0 not started. 1 is running. 2 is ended
    transfer_open = Column(Boolean, default=False)
    swap_open = Column(Boolean, default=False)
    current_day = Column(Integer, default=0)
    days = Column(Integer)
    stage1_start = Column(Integer)
    stage2_start = Column(Integer)
    url = Column(String(150))

    def __init__(self, id, name, days, stage1_start, stage2_start, url):
        self.id = id
        self.name = name
        self.days = days
        self.stage1_start = stage1_start
        self.stage2_start = stage2_start
        self.url = url
    

class LeagueUser(Base):
    __tablename__ = "league_user"
    id = Column(Integer, Sequence('id'), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    username = Column(String(50), ForeignKey(User.username), nullable=False)
    league = Column(Integer, ForeignKey(League.id), index=True)
    money = Column(Float, default=50.0)
    reserve_money = Column(Float, default=50.0)
    points = Column(Float, default=0.0)
    picks = Column(Integer, default=0)
    bans = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    points_rank = Column(Integer)
    wins_rank = Column(Integer)
    picks_rank = Column(Integer)
    bans_rank = Column(Integer)
    old_points_rank = Column(Integer)
    old_wins_rank = Column(Integer)
    old_picks_rank = Column(Integer)
    old_bans_rank = Column(Integer)
    last_change = Column(BigInteger, default=int(time.time()))

    def __init__(self, user_id, username, league):
        self.user_id = user_id
        self.username = username
        self.league = league


# # check if I should use polymorphic mapping for this with userLeague
class LeagueUserDay(Base):
    __tablename__ = "league_user_day"
    id = Column(Integer, Sequence('id'), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    username = Column(String(50), ForeignKey(User.username), nullable=False)
    league = Column(Integer, ForeignKey(League.id), index=True)
    day = Column(Integer, index=True)
    stage = Column(Integer)  # 0 qualifiers, 1 group stage, 2 main event
    money = Column(Float, default=50.0)
    points = Column(Float, default=0.0)
    picks = Column(Integer, default=0)
    bans = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    points_rank = Column(Integer)
    wins_rank = Column(Integer)
    picks_rank = Column(Integer)
    bans_rank = Column(Integer)

    def __init__(self, user_id, username, league, day, stage):
        self.user_id = user_id
        self.username = username
        self.league = league
        self.day = day
        self.stage = stage


class Friend(Base):
    __tablename__ = "friend_new"
    id = Column(Integer, Sequence('id'), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    friend = Column(Integer, ForeignKey(User.id), nullable=False)
    UniqueConstraint('user_id', 'friend')

    def __init__(self, user_id, friend):
        self.user_id = user_id
        self.friend = friend
    # Is some fucking fuckhead going to break this by adding themselves as a friend?
        # should also make user/friend be a unique pair. so cant friend twice


class OldFriend(Base):
    __tablename__ = "friend"
    friend_id = Column(Integer, Sequence('id'), primary_key=True)
    user = Column(String(50), ForeignKey(User.username), nullable=False)
    friend = Column(String(50), ForeignKey(User.username), nullable=False)

    def __init__(self, user, friend):
        self.user = user
        self.friend = friend


class Hero(Base):
    __tablename__ = "hero"
    id = Column(Integer, primary_key=True)  # api hero ids start at 1
    name = Column(String(100), nullable=False, index=True)  #index=true?
    league = Column(Integer, ForeignKey(League.id), primary_key=True, nullable=False)
    value = Column(Float, default=10.0)
    points = Column(Integer, default=0)
    picks = Column(Integer, default=0)
    bans = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    active = Column(Boolean, default=True)  # this is for when valve release patch midway through tournament and add/remove from cm
    UniqueConstraint('league', 'hero_id')

    # maybe I want day here as well? somewhere to track day value fluctuations

    def __init__(self, id, name, value, league):
        self.id = id
        self.name = name
        self.value = value
        self.league = league

    @property
    def username(self):
        # kind of hack to not have to refactor leaderboard pages
        return self.name


class TeamHero(Base):
    __tablename__ = "team_hero"
    id = Column(Integer, Sequence('id'), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    hero_id = Column(Integer, ForeignKey(Hero.id), index=True, nullable=False)
    # commented out due to mapper exception when joining Hero and TeamHero when multiple foreign keys
    # To make it work you give join a tuple I now believe. table, then table column to join I think
    hero_name = Column(String(100))#, ForeignKey(Hero.name))
    league = Column(Integer, ForeignKey(League.id), index=True, nullable=False)
    cost = Column(Float)
    reserve = Column(Boolean, index=True)
    UniqueConstraint('league', 'hero_id', 'user_id')

    def __init__(self, user_id, hero_id, league, cost, reserve, **kwargs):
        self.user_id = user_id
        self.hero_id = hero_id
        self.hero_name = kwargs.get("hero_name", (item for item in heroes if item["id"] == hero_id).next()["name"])
        self.league = league
        self.cost = cost
        self.reserve = reserve


class Sale(Base):
    __tablename__ = "sale"
    sale_id = Column(Integer, Sequence('sale_id'), primary_key=True)
    user = Column(Integer, ForeignKey('league_user.id'), nullable=False, index=True)  # index true?
    hero = Column(Integer, ForeignKey('hero.id'), nullable=False, index=True)
    league_id = Column(Integer, ForeignKey('league.id'), nullable=False, index=True)
    date = Column(DateTime, nullable=False, default=func.now())
    value = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    is_buy = Column(Boolean, nullable=False)

    def __init__(self, user, hero, league_id, value, cost, is_buy):
        self.user = user
        self.hero = hero
        self.league_id = league_id
        self.value = value
        self.cost = cost
        self.is_buy = is_buy


class Result(Base):
    __tablename__ = "result"
    id = Column(Integer, Sequence('id'), primary_key=True)
    match_id = Column(BigInteger, nullable=False, index=True)
    tournament_id = Column(Integer, nullable=False)
    hero = Column(Integer, nullable=False)
    result_str = Column(String(20), nullable=False)
    timestamp = Column(Integer)
    applied = Column(Integer, default=0)  # 1 is applied to heroes. 2 for leagues. 3 for battlecups
    series_id = Column(BigInteger)
    is_radiant = Column(Boolean)

    def __init__(self, tournament, hero, match, result_str, timestamp, series_id, is_radiant):
        self.tournament_id = tournament
        self.hero = hero
        self.match_id = match
        self.result_str = result_str
        self.timestamp = timestamp
        self.series_id = series_id
        self.is_radiant = is_radiant

    @staticmethod
    def result_to_value(result_str):
        points_dict = {
            "b1": 1,
            "b2": 2,
            "b3": 4,
            "p1l": -6,
            "p2l": -5,
            "p3l": -3,
            "p1w": 8,
            "p2w": 10,
            "p3w": 14,
        }
        return points_dict[result_str]


class Match(Base):
    __tablename__ = "match"
    match_id = Column(BigInteger, nullable=False, primary_key=True)
    radiant_team = Column(String(100), nullable=False)
    dire_team = Column(String(100), nullable=False)
    radiant_win = Column(Boolean, nullable=False)
    day = Column(Integer)

    def __init__(self, match_id, radiant_team, dire_team, radiant_win, day):
        self.match_id = match_id
        self.dire_team = dire_team
        self.radiant_team = radiant_team
        self.radiant_win = radiant_win
        self.day = day


class TeamHeroHistoric(Base):
    __tablename__ = "team_hero_historic"
    id = Column(Integer, Sequence('id'), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    hero_id = Column(Integer, ForeignKey(Hero.id), index=True, nullable=False)
    # commented out due to mapper exception when joining Hero and TeamHero when multiple foreign keys
    # To make it work you give join a tuple I now believe. table, then table column to join I think
    hero_name = Column(String(100))#, ForeignKey(Hero.name))
    league = Column(Integer, ForeignKey(League.id), index=True, nullable=False)
    cost = Column(Float)
    day = Column(Integer)
    UniqueConstraint('league', 'hero_id', 'user_id', 'day')

    def __init__(self, user_id, hero_id, league, cost, day, **kwargs):
        self.user_id = user_id
        self.hero_id = hero_id
        self.hero_name = kwargs.get("hero_name", (item for item in heroes if item["id"] == hero_id).next()["name"])
        self.league = league
        self.cost = cost
        self.day = day


# # check if I should use polymorphic mapping for this with userLeague
class HeroDay(Base):
    __tablename__ = "hero_day"
    id = Column(Integer, Sequence('id'), primary_key=True)
    hero_id = Column(Integer, ForeignKey(Hero.id), index=True, nullable=False)
    hero_name = Column(String(100), nullable=False)
    league = Column(Integer, ForeignKey(League.id), index=True)
    day = Column(Integer, index=True)
    stage = Column(Integer)  # 0 qualifiers, 1 group stage, 2 main event
    value = Column(Float)
    points = Column(Float, default=0.0)
    picks = Column(Integer, default=0)
    bans = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    points_rank = Column(Integer)
    wins_rank = Column(Integer)
    picks_rank = Column(Integer)
    bans_rank = Column(Integer)

    def __init__(self, hero_id, hero_name, league, day, stage, value):
        self.hero_id = hero_id
        self.hero_name = hero_name
        self.league = league
        self.day = day
        self.stage = stage
        self.value = value

    @property
    def username(self):
        # kind of hack to not have to refactor leaderboard pages
        return self.hero_name


# Guesser stuff


class HeroGame(Base):
    __tablename__ = "hero_game"
    id = Column(Integer, Sequence('id'), primary_key=True)
    match_id = Column(BigInteger, nullable=False, index=True)
    hero_id = Column(Integer, nullable=False, index=True)

    def __init__(self, match_id, hero_id):
        self.match_id = match_id
        self.hero_id = hero_id


class ItemBuild(Base):
    __tablename__ = "item_build"
    id = Column(Integer, Sequence('id'), primary_key=True)
    hero_game = Column(Integer, ForeignKey(HeroGame.id), index=True)
    item = Column(Integer, nullable=False, index=True)
    slot = Column(Integer, nullable=False, index=True)

    def __init__(self, hero_game, item, slot):
        self.hero_game = hero_game
        self.item = item
        self.slot = slot


class GuessUser(Base):
    __tablename__ = "guess_user"
    id = Column(Integer, Sequence('id'), primary_key=True)
    identifier_hash = Column(String(300), nullable=False, index=True)
    username = Column(String(40))
    last_roll = Column(DateTime, default=func.now(), nullable=False)
    streak = Column(Integer, default=0)
    max_streak = Column(Integer, default=0, index=True)
    current_hero_game = Column(Integer, ForeignKey(HeroGame.id), nullable=False)

    def __init__(self, identifier, current_hero_game):
        self.identifier_hash = identifier
        self.current_hero_game = current_hero_game

    def match_guess(self, session, guess):
        guess = ''.join([i for i in guess if i.isalpha()]).lower()
        current_hero = session.query(HeroGame.hero_id).filter(HeroGame.id == self.current_hero_game).first()[0]
        hero_string = [x["name"] for x in heroes if x["id"] == current_hero][0]
        hero_string = ''.join([i for i in hero_string if i.isalpha()]).lower()
        if hero_string == guess:
            return True

        items = session.query(ItemBuild).filter(ItemBuild.hero_game == current_hero).all()
        hero_guess_id = [x["id"] for x in heroes if
                         ''.join([i for i in x["name"] if i.isalpha()]).lower() == guess]
        if not hero_guess_id:
            return False
        else:
            hero_guess_id = hero_guess_id[0]

        valid = set()
        for i, item in enumerate(items):
            matching_games = set(x[0] for x in session.query(ItemBuild.hero_game).filter(ItemBuild.item == item.item)\
                .filter(ItemBuild.slot == item.slot).all())
            if i == 0:
                valid |= matching_games
            else:
                valid.intersection_update(matching_games)
        for id_ in valid:
            hero = session.query(HeroGame.hero_id).filter(HeroGame.id == id_).first()[0]
            if hero == hero_guess_id:
                return True
        return False

    def guess_in_time(self, now):
        # we need to set new_hero before load guess page again
        # otherwise you can exploit closing browser and reopen when dont know answer
        # therefore be a bit more lenient server-side with the timing. hence 34 not 30
        return now - self.last_roll <= datetime.timedelta(seconds=34)

