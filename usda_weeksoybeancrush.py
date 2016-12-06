from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Date,Float
from sqlalchemy.orm import sessionmaker
import requests
import re

url = 'https://www.ams.usda.gov/mnreports/gx_gr211.txt'
r = requests.get(url)
gx = r.content

OilPricePattern = re.compile(r'tank cars & trucks\\r\\nCentral IL\.\s+\S+\s+(\S+)\s+')
OilYieldPattern = re.compile(r'Oil yield per\\r\\nbushel crushed\s+\S+\s+(\S+)\s+')
OilValuePattern = re.compile(r'Value from bushel\\r\\nof soybeans\s+\S+\s+(\S+)\s+')
MealPricePattern = re.compile(r'unrestricted, bulk\\r\\nCentral IL\.\s+\S+\s+(\S+)\s+')
MealYieldPattern = re.compile(r'Meal yield per\\r\\nbushel crushed\s+\S+\s+(\S+)\s+')
SBValuePattern = re.compile(r'truck price Central\\r\\nIL\. points\s+\S+\s+(\S+)\s+')
EPVPattern = re.compile(r'Estimated Processing\\r\\nValue \(EPV\)\s+\S+\s+(\S+)\s+')
DatePattern = re.compile(r'Unit\s+(\S+\s\S+.\s\S+)\s+')

gxDate = DatePattern.search(str(gx)).group(1)
gxDate = datetime.strptime(gxDate,"%b %d, %Y").date()
OilPrice = float(OilPricePattern.search(str(gx)).group(1))
OilYield = float(OilYieldPattern.search(str(gx)).group(1))
OilValue = float(OilValuePattern.search(str(gx)).group(1))
MealPrice = float(MealPricePattern.search(str(gx)).group(1))
MealYield = float(MealYieldPattern.search(str(gx)).group(1))
SBValue = float(SBValuePattern.search(str(gx)).group(1))
EPV = float(EPVPattern.search(str(gx)).group(1))

MealValue = MealPrice * MealYield / 2204.6
OMValue = OilValue + MealValue
DiffOMSB = OMValue - SBValue

engine = create_engine('mysql+pymysql://root:root123@192.168.5.12:3306/data_analyze?charset=utf8', echo=True)

Base = declarative_base()


# 对象映射表
class ExportSale(Base):
    __tablename__ = 'usda_weeksoybeancrush'

    Date = Column(Date, primary_key=True)
    OilPrice = Column(Float)
    OilYield = Column(Float)
    OilValue = Column(Float)
    MealPrice = Column(Float)
    MealYield = Column(Float)
    MealValue = Column(Float)
    OMValue = Column(Float)
    SBValue = Column(Float)
    DiffOMSB = Column(Float)
    EPV = Column(Float)

    def __repr__(self):
        return 'the info is Date %s OilPrice is %s OilYield is %s and OilValue is %s' % (
            self.Date, self.OilPrice, self.OilYield, self.OilValue)


Session = sessionmaker(bind=engine)
session = Session()
try:

    temp = session.query(ExportSale).filter_by(Date=gxDate)

    #因为不需要覆盖旧数据，所以不用更新,当数据不存在的时候，直接add
    if temp is None:
        p = ExportSale(Date=gxDate,OilPrice=OilPrice,OilYield=OilYield,OilValue=OilValue,MealPrice=MealPrice,
                       MealYield=MealYield,MealValue=MealValue,OMValue=OMValue,SBValue=SBValue,DiffOMSB=DiffOMSB,EPV=EPV)
        session.add(p)
        session.commit()
except Exception:
    # 最好还是有个记录日志的东西，把日志记录一下
    pass