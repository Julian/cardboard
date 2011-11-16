import contextlib
import os.path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound


DB = os.path.join(os.path.dirname(__file__), "cards.db")

engine = create_engine("sqlite:///{}".format(DB))
Session = scoped_session(sessionmaker(bind=engine))


class Base(object):
    query = Session.query_property()

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(bind=engine, cls=Base)
