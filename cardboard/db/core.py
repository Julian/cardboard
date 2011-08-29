import os.path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB = os.path.join(os.path.dirname(__file__), "cards.db")

engine = create_engine('sqlite:///{}'.format(DB))
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
