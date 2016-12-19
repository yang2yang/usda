from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Float
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:root123@192.168.5.12:3306/demodb?charset=utf8',echo=True)

Base = declarative_base()

#connect session to active the action
Session = sessionmaker(bind=engine)
session = Session()

class Person(Base):
    __tablename__ = 'user'
    id2 = Column("id",Integer, primary_key=True)
    username = Column(String,nullable=False,default='')
    password = Column(String,nullable=False,default='')
    email = Column(String,nullable=False,default='')
    testdouble = Column(Float)

    def __repr__(self):
        return 'the info is ID %s Pname is %s Address is %s and Age is %s' % \
        (self.id2, self.username, self.password, self.email)



try:
    p = Person(id2=4, username='bruce', password='beijing', email="23", testdouble=None)
    session.add(p)
    session.commit()
except:
    session.close()

try:
    p = Person(id2=5, username='bruce', password='beijing', email="24", testdouble=None)
    session.add(p)
    session.commit()
except:
    pass

# p_1 = session.query(Person).filter_by(username='bruce').first()
# print(p_1)