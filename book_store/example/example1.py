# log SQL statements
import logging

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from book_store.db import db_engine

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String)


engine = db_engine.get_engine()

# create all tables
Base.metadata.create_all(engine)

############################# Case 1 ######################################
# Everything rollback

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

session.query(Person).delete()  # delete everything as case1

u1 = Person(name='Dave1')
session.add(u1)

# a nested section
session.begin_nested()

# another nested section
session.begin_nested()
u2 = Person(name='Steve1')
session.add(u2)
session.commit()

session.commit()

session.rollback()

session.close()

############################# Case 2 ######################################
# Everything is saved

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

u1 = Person(name='Dave2')
session.add(u1)

# a nested section
session.begin_nested()

# another nested section
session.begin_nested()
u2 = Person(name='Steve2')
session.add(u2)
session.commit()

session.commit()

session.commit()

session.close()

############################# Case 3 ######################################
# Outer only saved

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

u1 = Person(name='Dave3')
session.add(u1)

# a nested section
session.begin_nested()

# another nested section
session.begin_nested()
u2 = Person(name='Steve3')
session.add(u2)
session.commit()

session.rollback()

session.commit()

session.close()

############################# Case 4 ######################################
# Both saved without nested

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

u1 = Person(name='Dave4')
session.add(u1)
session.commit()

session = Session()
u2 = Person(name='Steve4')
session.add(u2)
session.commit()

session.close()

############################# Case 5 ######################################
# Saves nothing - Does not save not un-commmitted ones

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

u1 = Person(name='Dave5')
session.add(u1)

session = Session()
u2 = Person(name='Steve5')
session.add(u2)

session.close()

############################# Case 6 ######################################
# autocommit true when flush is called - saves everything

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
session.autocommit = True

u1 = Person(name='Dave6')
session.add(u1)

u2 = Person(name='Steve6')
session.add(u2)

session.flush()
session.close()

############################# Case 7 ######################################
# autocommit false when flush is called - does not save anything in db, query works in both case
# as by default autoFlush is true when entity is created

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
session.autocommit = False

u1 = Person(id=70, name='Dave7')
session.add(u1)

u2 = Person(id=71, name='Steve7')
session.add(u2)

getu1 = session.query(Person).get(70)
print("70---", getu1.__dict__)

getu2 = session.query(Person).get(71)
print("71---", getu2.__dict__)

session.flush()

getu1 = session.query(Person).get(70)
print("71--->", getu1.__dict__)

getu2 = session.query(Person).get(71)
print("70--->", getu2.__dict__)

session.close()

############################# Case 8 ######################################
# autoflush false when flush is called - does not save anything, query works in later case only

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
session.autoflush = False

u1 = Person(id=80, name='Dave8')
session.add(u1)

u2 = Person(id=81, name='Steve8')
session.add(u2)

getu1 = session.query(Person).get(80)
print("80---", getu1)

getu2 = session.query(Person).get(81)
print("81---", getu2)

session.flush()

getu1 = session.query(Person).get(80)
print("80--->", getu1.__dict__)

getu2 = session.query(Person).get(81)
print("81--->", getu2.__dict__)

session.close()

############################# Case 9 ######################################
# merge - updates record when commit if same id

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

u1 = Person(id=90, name='Dave9')
session.add(u1)

getu1 = session.query(Person).get(90)

print("91---", getu1.__dict__)
u2 = Person(id=91, name='Dave99')

session.merge(u2)

getu2 = session.query(Person).get(91)

print("90--->", getu1.__dict__)
print("91--->", getu2.__dict__)

session.commit()

session.close()

############################# Case 10 ######################################
# similar to above scenario with refresh (expire + query) - updates record when commit if same id

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
session.autoflush = False

u1 = Person(id=100, name='Dave10')
session.add(u1)
session.flush()
u1.name = 'Dave1010'

getu1 = session.query(Person).get(100)
print("10---", u1.__dict__)  # updated local value
print("10---", getu1.__dict__)  # updated local value

session.refresh(u1)  # read from db again

print("10--->", u1.__dict__)  # Back to Db value
print("10--->", getu1.__dict__)  # Back to Db value

session.close()
