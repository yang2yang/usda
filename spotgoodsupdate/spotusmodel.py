from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:root123@192.168.5.12:3306/data_analyze?charset=utf8', echo=True)

Base = declarative_base()

# connect session to active the action
Session = sessionmaker(bind=engine)
session = Session()


class SpotmarketUs(Base):
    __tablename__ = 'spotmarket_us'
    Commodity = Column(Integer, primary_key=True)
    Date = Column(Date, primary_key=True)
    Location = Column(String, primary_key=True)
    Category = Column(String)
    Variety = Column(String)
    GradeDescription = Column(String)
    Units = Column(String, primary_key=True)
    Transmode = Column(String, primary_key=True)
    BidLow = Column(Float)
    BidHigh = Column(Float)
    PricingPoint = Column(String, primary_key=True)
    DeliveryPeriod = Column(String, primary_key=True)
