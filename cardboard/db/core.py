import os.path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker


DB = os.path.join(os.path.dirname(__file__), "cards.db")


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


def get_or_create(model, session=None, defaults=(), **kwargs):
    commit = session is None

    if commit:
        session = Session()

    instance = session.query(model).filter_by(**kwargs).one()

    if instance is None:
        kwargs.update(defaults)
        instance = model(**kwargs)
        session.add(instance)

        if commit:
            session.commit()

    return instance


engine = create_engine('sqlite:///{}'.format(DB))
Base = declarative_base(bind=engine, cls=Base)
Session = sessionmaker(bind=engine)
