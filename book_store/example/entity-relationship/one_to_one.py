from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Float

from book_store.db import db_engine
# log SQL statements
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = db_engine.get_engine()
Session = db_engine.get_session()
session = Session()
Base = declarative_base(bind=engine)
Base.metadata.drop_all()


# One to One but it looks and behaves like one to many unless some validation is not added, from orm side it only
# generates warning in case of multiple record is found on either side uselist property is used which tells that
# property should be loaded as scalar -> which will kind of make sure its one to one instead of one to many


class Stop(Base):
    __tablename__ = 'stop'
    id = Column(Integer, primary_key=True, unique=True)
    tollbooth = relationship("Tollbooth", uselist=False, backref="stop")
    sequence = Column(Integer, default=111)


class Tollbooth(Base):
    __tablename__ = 'tollbooth'
    id = Column(Integer, primary_key=True, unique=True)
    stop_id = Column(Integer, ForeignKey('stop.id'))
    price = Column(Float)


Base.metadata.create_all()

stop = Stop(sequence=33)
tollbooth = Tollbooth(price=11.11)
stop.tollbooth = tollbooth
print("\n----stop5_1: {}".format(tollbooth.stop.__dict__))  # Works
print("\n----tollbooth5_1: {}".format(stop.tollbooth.stop.__dict__))  # Works

stop1 = Stop(sequence=33)
stop2 = Stop(sequence=34)
tollbooth = Tollbooth(price=11.11)
stop1.tollbooth = tollbooth
stop2.tollbooth = tollbooth
print("\n----stop15_2: {}".format(tollbooth.stop.__dict__))  # Works
print("\n----tollbooth15_2: {}".format(stop1.tollbooth.stop.__dict__))  # Works Remembers the last one
print("\n----tollbooth25_2: {}".format(stop2.tollbooth.stop.__dict__))  # Works
