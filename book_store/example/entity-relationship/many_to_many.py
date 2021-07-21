from sqlalchemy import Table, Column, Integer, ForeignKey, String
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

# ############################# Many to Many ######################################## M:N always can be think of as
# 1:M from both sides to one meeting side X => Left Entity 1:M -> X <- M:1 Right Entity this X can be labeled as
# association table => there is will be seperated entity/table which will basically store this association of two
# entities this association table is passed with secondary property in relationship, secondary also accepts callable
# for dynamic association table cascade properties can be used if auto-del is needed (only works from relationship
# side), otherwise manually remove would also work


car_stops = Table(
    'car_stops',
    Base.metadata,
    Column('stop_id', Integer, ForeignKey('stop.id')),
    Column('car_id', Integer, ForeignKey('car.id'))
)


class Stop(Base):
    __tablename__ = 'stop'
    id = Column(Integer, primary_key=True, unique=True)
    cars = relationship('Car', secondary=car_stops, back_populates='stops')
    sequence = Column(Integer, default=111)


class Car(Base):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True, unique=True)
    stops = relationship('Stop', secondary=car_stops, back_populates='cars')
    license_no = Column(String)


Base.metadata.create_all()

stop1 = Stop(sequence=11)
stop2 = Stop(sequence=22)
stop3 = Stop(sequence=33)
car = Car(license_no="ABC 123")
car.stops = [stop1, stop2, stop3]
session.add(car)  # saves car and stops both
session.commit()
print("\n----stops : {}".format(car.stops[0].__dict__))  # Works
print("\n----cars : {}".format(stop1.cars[0].__dict__))  # Works

stop1 = Stop(sequence=11)
stop2 = Stop(sequence=22)
stop3 = Stop(sequence=33)
car1 = Car(license_no="ABC 123")
car2 = Car(license_no="DEF 123")
car1.stops = [stop2, stop3]
car2.stops = [stop3]
session.add(car1, car2)
# saves car and stops both in db
session.commit()
print("\n----car 1 stops : {}".format(car1.stops[1].__dict__)) #Works
print("\n----car 2 stops : {}".format(car2.stops[0].__dict__)) #Works
print("\n----car1 : {}".format(stop3.cars[0].__dict__)) #Works
print("\n----car2 : {}".format(stop3.cars[1].__dict__)) #Works

