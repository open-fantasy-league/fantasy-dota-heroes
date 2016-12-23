import ConfigParser
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from fantasydota import Base
from zope.sqlalchemy import ZopeTransactionExtension


def make_session():

    config = ConfigParser.ConfigParser()
    config.read('development.ini')
    db_url = os.environ.get("FANTASYDOTA_DB")
    engine = create_engine(db_url, echo=False)
    DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    session = DBSession()
    return session
