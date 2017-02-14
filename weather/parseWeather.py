from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import os

engine = create_engine('mysql+pymysql://root:root123@192.168.5.12:3306/data_analyze?charset=utf8', echo=True)
engine = create_engine('mysql+pymysql://root:root123@192.168.2.23:3306/data_analyze?charset=utf8', echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


# 数据库映射类
class OOPP(Base):
    __tablename__ = 'oopp'
    stn = Column(String, primary_key=True)
    wbean = Column(String, primary_key=True)
    yearmoda = Column(Date, primary_key=True)
    temp = Column(Float)
    v0 = Column(Float)
    dewp = Column(Float)
    v1 = Column(Float)
    slp = Column(Float)
    v2 = Column(Float)
    stp = Column(Float)
    v3 = Column(Float)
    visib = Column(Float)
    v4 = Column(Float)
    wdsp = Column(Float)
    v5 = Column(Float)
    mxspd = Column(Float)
    gust = Column(Float)
    max = Column(Float)
    min = Column(Float)
    prcp = Column(Float)
    IG = Column(String)
    sndp = Column(Float)
    f = Column(Integer)
    r = Column(Integer)
    s = Column(Integer)
    h = Column(Integer)
    t = Column(Integer)
    t2 = Column(Integer)


# pattern = re.compile(r'(\d+)\D+(\d+)\D+(\d+)\D+(.+)\D+\d+(.+)\D+.+\D+(.+)\D+.+\D+(.+)\D+.+\D+(.+)\D+.+\D+(.+)\D+.+\D+(.+)\D+(.+)\D+(.+)\D+(.+)\D+(.+)\D+(.+)\D+(.+)')

# 得到Prcp除字母的一段
def getPrcp(str):
    if str[-1:].isalpha():
        return str[:-1]
    return str

# 得到Prcp的一段字母
def getIG(str):
    if str[-1:].isalpha():
        return str[-1:]
    return None

# 对每一个文件进行遍历
def add(fileName):
    flag = False
    with open(fileName) as f:
        for line in f.readlines():
            if not flag:
                flag = True
                continue
            # 按空格切分
            splitedLine = line.split()

            # for i in range(len(splitedLine)):
            #     print(i,splitedLine[i])

            p = OOPP(
                stn=splitedLine[0],
                wbean=splitedLine[1],
                yearmoda=time.strptime(splitedLine[2],"%Y%m%d"),
                temp=splitedLine[3],
                v0 = splitedLine[4],
                dewp=splitedLine[5],
                v1=splitedLine[6],
                slp=splitedLine[7],
                v2=splitedLine[8],
                stp=splitedLine[9],
                v3=splitedLine[10],
                visib=splitedLine[11],
                v4=splitedLine[12],
                wdsp=splitedLine[13],
                v5=splitedLine[14],
                mxspd=splitedLine[15],
                gust=splitedLine[16],
                # 如果有星号，需要把星号给去掉
                max=splitedLine[17].rstrip("*"),
                # 如果有星号，需要把星号给去掉
                min=splitedLine[18].rstrip("*"),
                # 需要把prcp中的数字给筛选出来
                prcp=getPrcp(splitedLine[19]),
                # 需要把prcp中的字母给筛选出来
                IG=getIG(splitedLine[19]),
                sndp=splitedLine[20],
                f=splitedLine[21][:1],
                r=splitedLine[21][1:2],
                s=splitedLine[21][2:3],
                h=splitedLine[21][3:4],
                t=splitedLine[21][4:5],
                t2=splitedLine[21][5:6],
            )

            session.add(p)
        try:

            session.commit()
            print(fileName,"is OK")
        except:
            session.rollback()
            session.close()
            pass


def Test2(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        print(path)
        if "op" in path[-2:]:
            add(path)
        if os.path.isdir(path):
            Test2(path)


Test2(r"C:\Users\admin\Desktop\现在的日度\日度")