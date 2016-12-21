from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Date, Column, String, Float,Integer

engine = create_engine('mysql+pymysql://root:root123@192.168.5.12:3306/data_analyze?charset=utf8', echo=True)

Base = declarative_base()


class SpotMarketChina(Base):
    __tablename__ = 'spotmarket_china'
    Commodity = Column(String, primary_key=True)
    Date = Column(Date)
    State = Column(String, default="")
    Region = Column(String)
    Price = Column(Float)

    def __repr__(self):
        return 'the info is Commodity %s Date is %s State is %s and Region is %s and Price is %s' % \
               (self.Commodity, self.Date, self.State, self.Region, self.Price)


class StateRegion(Base):
    __tablename__ = "state_region"
    id = Column(Integer,primary_key=True,autoincrement=True)
    agri_type = Column(String)
    agri_state = Column(String)
    agri_region = Column(String)



Session = sessionmaker(bind=engine)
session = Session()
