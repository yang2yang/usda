from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import sessionmaker
import csv
import time

startTime = time.time()

engine = create_engine('mysql+pymysql://root:root123@192.168.5.12:3306/data_analyze?charset=utf8', echo=True)

Base = declarative_base()


# 对象映射表
class Fgis(Base):
    __tablename__ = 'usda_fgis'

    Thursday = Column(Date, primary_key=True)
    SerialNo = Column(Integer, primary_key=True)
    TypeShipm = Column(String)
    TypeServ = Column(String)
    CertDate = Column(Date)
    TypeCarrier = Column(Integer)
    CarrierName = Column(String)
    Grade = Column(String)
    Grain = Column(String)
    Class = Column(String)
    SubClass = Column(String)
    SpecGr1 = Column(String)
    SpecGr2 = Column(String)
    Pounds = Column(Float)
    Destination = Column(String)
    SublCarrs = Column(Float)
    FieldOffice = Column(String)
    Port = Column(String)
    AMSReg = Column(String)
    FGISReg = Column(String)
    City = Column(String)
    State = Column(String)
    MKTYR = Column(Float)
    DKGHIGH = Column(Float)
    DKGLOW = Column(Float)
    DKGAVG = Column(Float)
    TW = Column(Float)
    MLDORD = Column(String)
    MLD = Column(Float)
    MHIGH = Column(Float)
    MLOW = Column(Float)
    MAVG = Column(Float)
    DHVHVACHARD = Column(Float)
    OWH = Column(Float)
    WC = Column(Float)
    HT = Column(Float)
    DKT = Column(Float)
    FM = Column(Float)
    SHBN = Column(Float)
    DEF = Column(Float)
    CCL = Column(Float)
    WOCL = Column(Float)
    PLDORD = Column(String)
    PLD = Column(Float)
    PBASIS = Column(String)
    PSPM = Column(Float)
    PHIGH = Column(Float)
    PLOW = Column(Float)
    PAVG = Column(Float)
    FNBASIS = Column(String)
    FNSPM = Column(Float)
    FN = Column(Float)
    SUBLWINS = Column(Float)
    COMPINF = Column(Float)
    INSINLOT = Column(Float)
    Insecticide = Column(String)
    DUSTSUPR = Column(String)
    DYE = Column(String)
    Fumigant = Column(String)
    OCOL = Column(Float)
    AFLAPERF = Column(String)
    SPL = Column(Float)
    BNFM = Column(Float)
    SBLY = Column(Float)
    THIN = Column(Float)
    BN = Column(Float)
    BB = Column(Float)
    SKBN = Column(Float)
    WO = Column(Float)
    SMUT = Column(Float)
    PL = Column(Float)
    OG = Column(Float)
    HTMJ = Column(Float)
    HTMI = Column(Float)
    FMJ = Column(Float)
    FMI = Column(Float)
    MMJ = Column(Float)
    MMI = Column(Float)
    DH = Column(Float)
    OAVG = Column(Float)
    AD = Column(Float)
    FMOW = Column(Float)
    SO = Column(Float)
    FMOWR = Column(Float)
    Bushels = Column(Float)  # 不对的这个名字1000Bushels
    MetricTon = Column(Float)
    DKGCERT = Column(Float)
    BCFM = Column(Float)
    OLDORD = Column(String)
    OBASIS = Column(String)
    BC = Column(Float)
    OSP = Column(Float)
    OLD = Column(Float)
    OHIGH = Column(Float)
    OLOW = Column(Float)
    AFLAREQ = Column(String)
    AFLABASIS = Column(String)
    AFLASCRN = Column(Float)
    AFLASCNP = Column(Float)
    AFLAQTN = Column(Float)
    AFLAQTP = Column(Float)
    AFLAAVGPPB = Column(Float)
    AFLAREJ = Column(Float)
    WHARD = Column(Float)
    PLDORD2 = Column(String)
    PLD2 = Column(Float)
    DONREQ = Column(String)
    DONBASIS = Column(String)
    DONQL = Column(Float)
    DONQT = Column(Float)
    DONAVGPPM = Column(Float)
    DONREJ = Column(Float)

    def __repr__(self):
        return 'the info is Thursday %s SerialNo is %s EndStart is %s and Country is %s' % (
            self.Thursday, self.SerialNo, self.EndStart, self.Country)


Session = sessionmaker(bind=engine)
session = Session()

# exportSale = session.query(ExportSale).filter_by(Thursday="2006-01-05").first()

with open('fgis/CY2016.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 'Thursday':
            continue

        # 从cvs解析出来的全部都是str，跟excel不同
        # 因为将空字符串放入数据库会报错，转化为null
        for index, value in enumerate(row):
            if value == '':
                row[index] = None

        # Thursday 原来是19950101字符串需要转化
        row[0] = datetime.strptime(row[0], '%Y%m%d').date()
        # CertDate 原来是19950101字符串需要转化
        row[4] = datetime.strptime(row[4], '%Y%m%d').date()

        f = session.query(Fgis).filter_by(Thursday=row[0], SerialNo=row[1]).first()
        if f is not None:
            f.TypeShipm = row[2]
            f.TypeServ = row[3]
            f.CertDate = row[4]
            f.TypeCarrier = row[5]
            f.CarrierName = row[6]
            f.Grade = row[7]
            f.Grain = row[8]
            f.Class = row[9]
            f.SubClass = row[10]
            f.SpecGr1 = row[11]
            f.SpecGr2 = row[12]
            f.Pounds = row[13]
            f.Destination = row[14]
            f.SublCarrs = row[15]
            f.FieldOffice = row[16]
            f.Port = row[17]
            f.AMSReg = row[18]
            f.FGISReg = row[19]
            f.City = row[20]
            f.State = row[21]
            f.MKTYR = row[22]
            f.DKGHIGH = row[23]
            f.DKGLOW = row[24]
            f.DKGAVG = row[25]
            f.TW = row[26]
            f.MLDORD = row[27]
            f.MLD = row[28]
            f.MHIGH = row[29]
            f.MLOW = row[30]
            f.MAVG = row[31]
            f.DHVHVACHARD = row[32]
            f.OWH = row[33]
            f.WC = row[34]
            f.HT = row[35]
            f.DKT = row[36]
            f.FM = row[37]
            f.SHBN = row[38]
            f.DEF = row[39]
            f.CCL = row[40]
            f.WOCL = row[41]
            f.PLDORD = row[42]
            f.PLD = row[43]
            f.PBASIS = row[44]
            f.PSPM = row[45]
            f.PHIGH = row[46]
            f.PLOW = row[47]
            f.PAVG = row[48]
            f.FNBASIS = row[49]
            f.FNSPM = row[50]
            f.FN = row[51]
            f.SUBLWINS = row[52]
            f.COMPINF = row[53]
            f.INSINLOT = row[54]
            f.Insecticide = row[55]
            f.DUSTSUPR = row[56]
            f.DYE = row[57]
            f.Fumigant = row[58]
            f.OCOL = row[59]
            f.AFLAPERF = row[60]
            f.SPL = row[61]
            f.BNFM = row[62]
            f.SBLY = row[63]
            f.THIN = row[64]
            f.BN = row[65]
            f.BB = row[66]
            f.SKBN = row[67]
            f.WO = row[68]
            f.SMUT = row[69]
            f.PL = row[70]
            f.OG = row[71]
            f.HTMJ = row[72]
            f.HTMI = row[73]
            f.FMJ = row[74]
            f.FMI = row[75]
            f.MMJ = row[76]
            f.MMI = row[77]
            f.DH = row[78]
            f.OAVG = row[79]
            f.AD = row[80]
            f.FMOW = row[81]
            f.SO = row[82]
            f.FMOWR = row[83]
            f.Bushels = row[84]
            f.MetricTon = row[85]
            f.DKGCERT = row[86]
            f.BCFM = row[87]
            f.OLDORD = row[88]
            f.OBASIS = row[89]
            f.BC = row[90]
            f.OSP = row[91]
            f.OLD = row[92]
            f.OHIGH = row[93]
            f.OLOW = row[94]
            f.AFLAREQ = row[95]
            f.AFLABASIS = row[96]
            f.AFLASCRN = row[97]
            f.AFLASCNP = row[98]
            f.AFLAQTN = row[99]
            f.AFLAQTP = row[100]
            f.AFLAAVGPPB = row[101]
            f.AFLAREJ = row[102]
            f.WHARD = row[103]
            f.PLDORD2 = row[104]
            f.PLD2 = row[105]
            f.DONREQ = row[106]
            f.DONBASIS = row[107]
            f.DONQL = row[108]
            f.DONQT = row[109]
            f.DONAVGPPM = row[110]
            f.DONREJ = row[111]

            session.commit()
        else:
            fgis = Fgis(
                Thursday=row[0],
                SerialNo=row[1],
                TypeShipm=row[2],
                TypeServ=row[3],
                CertDate=row[4],
                TypeCarrier=row[5],
                CarrierName=row[6],
                Grade=row[7],
                Grain=row[8],
                Class=row[9],
                SubClass=row[10],
                SpecGr1=row[11],
                SpecGr2=row[12],
                Pounds=row[13],
                Destination=row[14],
                SublCarrs=row[15],
                FieldOffice=row[16],
                Port=row[17],
                AMSReg=row[18],
                FGISReg=row[19],
                City=row[20],
                State=row[21],
                MKTYR=row[22],
                DKGHIGH=row[23],
                DKGLOW=row[24],
                DKGAVG=row[25],
                TW=row[26],
                MLDORD=row[27],
                MLD=row[28],
                MHIGH=row[29],
                MLOW=row[30],
                MAVG=row[31],
                DHVHVACHARD=row[32],
                OWH=row[33],
                WC=row[34],
                HT=row[35],
                DKT=row[36],
                FM=row[37],
                SHBN=row[38],
                DEF=row[39],
                CCL=row[40],
                WOCL=row[41],
                PLDORD=row[42],
                PLD=row[43],
                PBASIS=row[44],
                PSPM=row[45],
                PHIGH=row[46],
                PLOW=row[47],
                PAVG=row[48],
                FNBASIS=row[49],
                FNSPM=row[50],
                FN=row[51],
                SUBLWINS=row[52],
                COMPINF=row[53],
                INSINLOT=row[54],
                Insecticide=row[55],
                DUSTSUPR=row[56],
                DYE=row[57],
                Fumigant=row[58],
                OCOL=row[59],
                AFLAPERF=row[60],
                SPL=row[61],
                BNFM=row[62],
                SBLY=row[63],
                THIN=row[64],
                BN=row[65],
                BB=row[66],
                SKBN=row[67],
                WO=row[68],
                SMUT=row[69],
                PL=row[70],
                OG=row[71],
                HTMJ=row[72],
                HTMI=row[73],
                FMJ=row[74],
                FMI=row[75],
                MMJ=row[76],
                MMI=row[77],
                DH=row[78],
                OAVG=row[79],
                AD=row[80],
                FMOW=row[81],
                SO=row[82],
                FMOWR=row[83],
                Bushels=row[84],
                MetricTon=row[85],
                DKGCERT=row[86],
                BCFM=row[87],
                OLDORD=row[88],
                OBASIS=row[89],
                BC=row[90],
                OSP=row[91],
                OLD=row[92],
                OHIGH=row[93],
                OLOW=row[94],
                AFLAREQ=row[95],
                AFLABASIS=row[96],
                AFLASCRN=row[97],
                AFLASCNP=row[98],
                AFLAQTN=row[99],
                AFLAQTP=row[100],
                AFLAAVGPPB=row[101],
                AFLAREJ=row[102],
                WHARD=row[103],
                PLDORD2=row[104],
                PLD2=row[105],
                DONREQ=row[106],
                DONBASIS=row[107],
                DONQL=row[108],
                DONQT=row[109],
                DONAVGPPM=row[110],
                DONREJ=row[111])

            session.add(fgis)

            session.commit()

endTime = time.time()

print("本次运行耗时:%s秒,%s分" % (endTime - startTime, (endTime - startTime) / 60))
