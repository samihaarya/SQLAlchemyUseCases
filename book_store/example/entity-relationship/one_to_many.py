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

# -----  case -1 ------------
# - relationship on one side, entity populated on one side + unidirectional approach, without backref and backpopulates

Base.metadata.clear()
Base = declarative_base(bind=engine)


class Route(Base):
    __tablename__ = 'route'
    id = Column(Integer, primary_key=True, unique=True)
    stops = relationship("Stop")
    note = Column(String)


class Stop(Base):
    __tablename__ = 'stop'
    id = Column(Integer, primary_key=True, unique=True)
    route_id = Column(Integer, ForeignKey('route.id'))
    sequence = Column(Integer, default='1')


Base.metadata.create_all()

route = Route()
session.add(route)
session.commit()
stop = Stop(route_id=route.id)
session.add(stop)
session.commit()
print("\n----stops2_1: {}".format(route.stops[0].__dict__))  # Works
# print("\n----route_1: {}".format(stop.route.__dict__))  # Does not Work


route = Route()
session.add(route)
session.commit()
stop = Stop()
session.add(stop)
route.stops.append(stop)
session.commit()
print("\n----stops2_2: {}".format(route.stops[0].__dict__))  # Works
# print("\n----route_2: {}".format(stop.route.__dict__))  # does not Work
#
# # print('yayaya')
#
# route = Route()
# session.add(route)
# session.commit()
# stop = Stop()
# stop.route_id = route.id
# session.add(stop)
# session.commit()
# # print(stop.route.__dict__)  # Does not Work, no route instance
# print(route.stops[0].__dict__)  # Works
#
# # To compare with back populate case
# route = Route()
# stop = Stop(sequence=2)
# stop.route_id = route.id
# print("\n----stops2_3: {}".format(
#     route.stops))  # empty, Does not work - with or without commit route does not know that stop is added to it
# print("\n----route_3: {}".format(stop.__dict__))  # Works


#  ------- case-2 -----------
# # - relationship on one side, entity populated on one side + bidirectional approach, with backref backref on either
# # side has exact same effect - but ideally it is kept on parent side so child can use that field - some IDE does not
# # support that
Base.metadata.clear()
Base = declarative_base(bind=engine)


class Route(Base):
    __tablename__ = 'route'
    id = Column(Integer, primary_key=True, unique=True)
    stops = relationship("Stop", backref='route')
    note = Column(String)


class Stop(Base):
    __tablename__ = 'stop'
    id = Column(Integer, primary_key=True, unique=True)
    route_id = Column(Integer, ForeignKey('route.id'))
    sequence = Column(Integer, default=111)


Base.metadata.create_all()

route = Route()
session.add(route)
session.commit()
stop = Stop(route_id=route.id)
session.add(stop)
session.commit()
print("\n----stops3_1: {}".format(route.stops[0].__dict__))  # Works
print("\n----route3_1: {}".format(stop.route.__dict__))  # Works

route = Route()
session.add(route)
session.commit()
stop = Stop()
session.add(stop)
route.stops.append(stop)
session.commit()
print("\n----stops3_2: {}".format(route.stops[0].__dict__))  # Works
print("\n----route3_2: {}".format(stop.route.__dict__))  # Works

route = Route()
session.add(route)
session.commit()
stop = Stop()
stop.route = route
session.add(stop)
session.commit()
print("\n----stops3_3: {}".format(route.stops[0].__dict__))  # Works
print("\n----route3_3: {}".format(stop.route.__dict__))  # Works

# ----- case-3 ----------
# bidirectional approach, with back_populates should be added on both side, tells both entities and can be saved in
# either way - backref can also work, kind of alternative
Base.metadata.clear()
Base = declarative_base(bind=engine)


class Route(Base):
    __tablename__ = 'route'
    id = Column(Integer, primary_key=True, unique=True)
    stops = relationship("Stop", back_populates='route')
    note = Column(String)


class Stop(Base):
    __tablename__ = 'stop'
    id = Column(Integer, primary_key=True, unique=True)
    route_id = Column(Integer, ForeignKey('route.id'))
    route = relationship("Route", back_populates='stops')
    sequence = Column(Integer, default=111)


Base.metadata.create_all()

route = Route()
stop1 = Stop()
stop2 = Stop()
# stop1.route = route
route.stops = [stop2, stop1]
print("\n----stops4: {}".format(route.stops[0].__dict__))  # Works
print("\n----route4: {}".format(stop1.route.__dict__))  # Works
