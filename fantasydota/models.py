from fantasydota.lib.constants import FESPORT_ACCOUNT
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
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import ZopeTransactionExtension

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
    account_type = Column(Integer, default=FESPORT_ACCOUNT, index=True)
    # 0 is regular. 1 steam, 2 reddit
    # unique on account_type 0 and username

    def __init__(self, username, account_type, password="", email=""):
        self.username = username
        self.password = bcrypt.encrypt(password)
        self.email = email
        self.account_type = account_type

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


class Friend(Base):
    # TODO move friend_new to friend in db
    __tablename__ = "friend"
    id = Column(Integer, Sequence('id'), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    friend = Column(Integer, ForeignKey(User.id), nullable=False)
    UniqueConstraint('user_id', 'friend')

    def __init__(self, user_id, friend):
        self.user_id = user_id
        self.friend = friend
    # Is some fucking fuckhead going to break this by adding themselves as a friend?
        # should also make user/friend be a unique pair. so cant friend twice

    # @staticmethod
    # def result_to_value(result_str):
    #     points_dict = {
    #         "b1": 1,
    #         "b2": 2,
    #         "b3": 4,
    #         "p1l": -5,
    #         "p2l": -4,
    #         "p3l": -2,
    #         "p1w": 9,
    #         "p2w": 11,
    #         "p3w": 15,
    #     }
    #     return points_dict[result_str]
    #
    # @staticmethod
    # def result_to_value_pubg(result_str):
    #     position, kills = result_str.split(",")
    #     position, kills = int(position), int(kills)
    #     score = kills * 2
    #     if position <= 1:
    #         score += 5
    #     elif position <= 3:
    #         score += 3
    #     elif position <= 5:
    #         score += 2
    #     elif position <= 10:
    #         score += 1
    #     return score


class Notification(Base):
    __tablename__ = "notification"
    id = Column(Integer, Sequence('id'), primary_key=True)
    user = Column(Integer, ForeignKey(User.id), index=True)
    seen = Column(Boolean, default=False, index=True)
    message = Column(String(100), nullable=False)
    link = Column(String(100), default='')

    def __init__(self, user, message, link=''):
        self.user = user
        self.message = message
        self.link = link
