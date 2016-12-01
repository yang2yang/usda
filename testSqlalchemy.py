from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:root123@192.168.5.12:3306/demodb?charset=utf8',echo=True)

Base = declarative_base()

#connect session to active the action
Session = sessionmaker(bind=engine)
session = Session()

class Person(Base):
    __tablename__ = 'user'
    id2 = Column("id",Integer, primary_key=True, autoincrement=True)
    username = Column(String,nullable=False,default='')
    password = Column(String,nullable=False,default='')
    email = Column(String,nullable=False,default='')

    def __repr__(self):
        return 'the info is ID %s Pname is %s Address is %s and Age is %s' % \
        (self.id2, self.username, self.password, self.email)

p = Person(username='bruce', password='beijing', email="22")
session.add(p)
session.commit()

p_1 = session.query(Person).filter_by(username='bruce').first()
print(p_1)