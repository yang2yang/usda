from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
import xlrd

engine = create_engine('mysql+pymysql://root:root123@192.168.5.12:3306/data_analyze?charset=utf8', echo=True)

Base = declarative_base()


# 对象映射表
class ExportSale(Base):
    __tablename__ = 'usda_exportsale_copy'

    Commodity = Column(String, primary_key=True)
    Date = Column(Date, primary_key=True)
    EndStart = Column(String)
    Country = Column(String, primary_key=True)
    WeeklyExports = Column(Integer)
    AccumExports = Column(Integer)
    CMYOutstandingSales = Column(Integer)
    CMYGrossSales = Column(Integer)
    CMYNetSales = Column(Integer)
    CMYTotalCommitments = Column(Integer)
    NMYOutstandingSales = Column(Integer)
    NMYNetSales = Column(Integer)
    UnitDesc = Column(String)
    CMY = Column(Integer, primary_key=True)
    NMY = Column(Integer)

    def __repr__(self):
        return 'the info is Commodity %s Date is %s EndStart is %s and Country is %s' % (
            self.Commodity, self.Date, self.EndStart, self.Country)


# connect session to active the action
Session = sessionmaker(bind=engine)
session = Session()

fileName = "ExportSalesDataByCommodity1.xls"

data = xlrd.open_workbook(fileName)

table = data.sheets()[0]

initYear = 2014


def getCMY(current, next):
    global initYear
    if next is not None:
        if current == "" and next == "STARTING MY":
            initYear += 1
        elif current == "ENDING MY" and next == "STARTING MY":
            initYear += 1
        elif current == "STARTING MY" and next == "":
            initYear += 1
    return initYear


# ['', 'Soybeans', 42327.0, '', 'BANGLADESH', 952.0, 163866.0, 169224.0, 55000.0, 55000.0, 333090.0, 0.0, 0.0, 'Metric Tons']
for i in range(7, table.nrows):
    recode = table.row_values(i)
    recode[2] = xlrd.xldate.xldate_as_datetime(recode[2], 0).date()

    if i + 1 < table.nrows:
        CMY = getCMY(recode[3], table.row_values(i + 1)[3])
    else:
        CMY = getCMY(recode[3], None)

    NMY = str(int(CMY) + 1)

    print(recode[2])
    print(i)

    exportSale = session.query(ExportSale).filter_by(Commodity=recode[1],Date=recode[2],Country=recode[4],CMY=CMY).first()
    if exportSale is not None:
        exportSale.EndStart = recode[3]
        exportSale.WeeklyExports = recode[5]
        exportSale.AccumExports = recode[6]
        exportSale.CMYOutstandingSales = recode[7]
        exportSale.CMYGrossSales = recode[8]
        exportSale.CMYNetSales = recode[9]
        exportSale.CMYTotalCommitments = recode[10]
        exportSale.NMYOutstandingSales = recode[11]
        exportSale.NMYNetSales = recode[12]
        exportSale.UnitDesc = recode[13]
        exportSale.CMY = CMY
        exportSale.NMY = NMY
        session.commit()
    else:
        p = ExportSale(Commodity=recode[1], Date=recode[2], EndStart=recode[3], Country=recode[4],
                       WeeklyExports=recode[5], AccumExports=recode[6], CMYOutstandingSales=recode[7],
                       CMYGrossSales=recode[8], CMYNetSales=recode[9], CMYTotalCommitments=recode[10],
                       NMYOutstandingSales=recode[11],
                       NMYNetSales=recode[12], UnitDesc=recode[13], CMY=CMY, NMY=NMY)
        session.add(p)
        session.commit()
