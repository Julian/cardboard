import os.path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker


DB = os.path.join(os.path.dirname(__file__), "cards.db")


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


engine = create_engine('sqlite:///{}'.format(DB))
Base = declarative_base(bind=engine, cls=Base)
Session = sessionmaker(bind=engine)
