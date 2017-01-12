import ConfigParser
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from fantasydota import Base


def make_session(transaction=True, autoflush=False, autocommit=False):
    # Yeah the arguments and their naming is so terrible. sorry
    config = ConfigParser.ConfigParser()
    config.read('development.ini')
    db_url = os.environ.get("FANTASYDOTA_DB") + "3"
    engine = create_engine(db_url, echo=False)
    if transaction:
        DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
    else:
        DBSession = sessionmaker(autoflush=autoflush, autocommit=autocommit)
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    session = DBSession()
    return session
