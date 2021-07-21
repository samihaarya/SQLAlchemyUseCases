from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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


Base.metadata.clear()

#  ------ case-1 ------------------
#
# class Route(Base):
#     __tablename__ = 'route'
#     id = Column(Integer, primary_key=True, unique=True)
#     stops = relationship("Stop", back_populates='route', lazy='select')
#     note = Column(String)
#
# class Stop(Base):
#     __tablename__ = 'stop'
#     id = Column(Integer, primary_key=True, unique=True)
#     route_id = Column(Integer, ForeignKey('route.id'))
#     route = relationship("Route", back_populates='stops')
#     sequence = Column(Integer, default=111)
#
#
# Base.metadata.create_all()
#
# route = Route(id=88)
# stop = Stop()
# stop.route = route
# session.add(route)
# session.add(stop)
# session.commit()
# session.close()
#
# session.begin()
# r = session.query(Route).get(88)
# print("\n----lazy -- route: {}".format(r.__dict__))  # Works
# print("\n----lazy -- stops2: {}".format(r.stops[0].__dict__))  # Works
#


# -------EAGER ---------------
Base.metadata.drop_all()
#
class Route(Base):
    __tablename__ = 'route'
    id = Column(Integer, primary_key=True, unique=True)
    stops = relationship("Stop", back_populates='route', lazy='joined')
    note = Column(String)

class Stop(Base):
    __tablename__ = 'stop'
    id = Column(Integer, primary_key=True, unique=True)
    route_id = Column(Integer, ForeignKey('route.id'))
    route = relationship("Route", back_populates='stops')
    sequence = Column(Integer, default=111)


Base.metadata.create_all()

route = Route(id=91)
stop = Stop()
stop.route = route
session.add(route)
session.add(stop)
session.commit()
session.close()
session.begin()
r = session.query(Route).get(91)
print("\n----Eager - route: {}".format(r.__dict__))  # Works
print("\n----Eager - stops2: {}".format(r.stops[0].__dict__))  # Works

