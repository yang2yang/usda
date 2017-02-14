import WindPy
import datetime
import time
import threading
from enum import Enum
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Float, Integer
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class daydata_echart(Base):
    __tablename__ = 'daydata'
    code = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    amt = Column(Float)
    chg = Column(Float)
    pct_chg = Column(Float)
    oi = Column(Integer)


# 切分list 利用的是生成器生成
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class DataScrapy:
    # codes表示需要抓取的code条码，codetype表示是否是分钟数据
    def __init__(self, codes, codetype):
        self.getSession()
        self.codetype = codetype
        self.flag = "open,high,low,close,volume,amt,chg,pct_chg,oi"
        self.codes = codes
        self.today = datetime.date.today()  # 获取今天日期
        self.deltadays = datetime.timedelta(days=3)  # 确定日期差额，如前天 days=2
        self.yesterday = self.today - self.deltadays  # 获取差额日期，昨天
        self.today = '2017-01-24'
        # self.yesterday = '1990-01-01'
        self.month = {"F": 1, "H": 3, "K": 5, "N": 7, "Q": 8, "U": 9, "V": 10, "X": 11, "Z": 12}

    # 获得数据库的连接和cursor
    def getSession(self):
        engine = create_engine(
            # 'mysql+pymysql://rootrun:R0ot#cC2016@12JK*7H3fj@rm-uf64r530b3fpwuhnro.mysql.rds.aliyuncs.com:3399/data_analyze?charset=utf8',
            'mysql+pymysql://root:root123@192.168.5.12:3306/data_analyze?charset=utf8',
            echo=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    # 保存数据到数据库中
    def saveData(self, outdata, code):
        if outdata.ErrorCode != 0:
            failcodes.append([code, outdata.ErrorCode])
            return

        for i in range(len(outdata.Data[0])):
            if self.isSuccess(code, outdata.Times[i]) and int(100 * outdata.Data[0][i]) != 0 and int(
                            100 * outdata.Data[1][i]) != 0 and int(
                        100 * outdata.Data[2][i]) != 0 and int(100 * outdata.Data[3][i]) != 0:
                if "RO" in code :
                    code = "OI" + code[2:]

                if len(code) == 9 and ("CZC" in code):
                    code = code[:2] + "1" + code[2:]

                p = daydata_echart(code=code,
                                   date=outdata.Times[i],
                                   open=outdata.Data[0][i],
                                   high=outdata.Data[1][i],
                                   low=outdata.Data[2][i],
                                   close=outdata.Data[3][i],
                                   volume=outdata.Data[4][i],
                                   amt=outdata.Data[5][i],
                                   chg=outdata.Data[6][i],
                                   pct_chg=outdata.Data[7][i],
                                   oi=outdata.Data[8][i])
                self.session.add(p)
                # 这样的话，每一个线程都是一个session，但是每一次commit都是一个特定时间内的完整的一个code
                # 因为可能会有部分数据出现重复，所以对每一条数据都进行commit
                try:
                    self.session.commit()
                except:
                    print("p.code=", code, "p.date", outdata.Times[i])
                    self.session.close()

    # 判断是否符合连续合约的条件
    def isSuccess(self, code, theDate):
        # BOF17E.CBT  SF17E.CBT
        if code[-4:] == '.CBT' and (code[:2] == 'BO' or code[:2] == 'SM' or code[:1] == 'S'):
            codeYear = int(code[-7:-5])
            codeMon = self.month[code[-8:-7]]

            theDateYear = int(str(theDate.year)[-2:])
            theDateMon = theDate.month
            theDateDay = theDate.day

            return self.__isSuccess(codeYear, codeMon, theDateYear, theDateMon, theDateDay)
        # A1701.DCE
        elif code[-4:] == '.DCE' and code[:1] == 'A':
            codeYear = int(code[-8:-6])
            codeMon = int(code[-6:-4])

            theDateYear = int(str(theDate.year)[-2:])
            theDateMon = theDate.month
            theDateDay = theDate.day

            return self.__isSuccess(codeYear, codeMon, theDateYear, theDateMon, theDateDay)
        else:
            return True

    def __isSuccess(self, codeYear, codeMon, theDateYear, theDateMon, theDateDay):
        if theDateMon == codeMon:
            if theDateDay >= 15:
                if codeYear == theDateYear + 1:
                    return True
                else:
                    return False
            else:
                if codeYear == theDateYear:
                    return True
                else:
                    return False
        elif theDateMon > codeMon:
            if codeYear == theDateYear + 1:
                return True
            else:
                return False
        else:
            if codeYear == theDateYear:
                return True
            else:
                return False

    # 线程中被运行的run方法
    def run(self):

        if self.codetype == False:
            for code in self.codes:
                self.saveData(WindPy.w.wsd(code, self.flag, str(self.yesterday), str(self.today), "", showblank=0),
                              code)


# CBOT,ICE
def getCbotIce():
    codes = []
    # 年份表示90年到23年的合约
    list0 = ['16', '17', '18', '19']
    # 国外的月份时间表示
    list4 = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z']
    list4 = {"F", "H", "K", "N", "Q", "U", "V", "X", "Z"}

    # 国外ICE和CME，另外代码中都是有E的
    cbt = ['S', 'C', 'BO', 'SM', 'ZE', 'W', 'RR', 'O']
    cbt = ['S', 'SM', 'BO']
    nice = ['SB', 'KC', 'CT', 'CC', 'DX']

    for a in nice:
        for b in list4:
            for c in list0:
                icecodes = a + b + c + "E" + ".NYB"
                # codes.append(icecodes)
    for a in cbt:
        for b in list4:
            for c in list0:
                icecodes = a + b + c + "E" + ".CBT"
                codes.append(icecodes)
    return codes


# CME
def getCme():
    codes = []
    CME = Enum('CME', [('ECME', 'E.CME'), ('CME', '.CME')])
    # 年份表示90年到23年的合约
    list0 = ['16', '17', '18', '19']
    cme = ['LC', 'FC', 'LH', 'DA']

    # 单独拿出来有E的
    # 无复用性
    for a in list0:
        codes.append('FC' + 'J' + a + CME.ECME.value)
        codes.append('DA' + 'J' + a + CME.ECME.value)
        for b in ['Z', 'J']:
            codes.append('LC' + b + a + CME.ECME.value)
            codes.append('LH' + b + a + CME.ECME.value)

    # 没E的
    for a in list0:
        for b in ['V', 'G', 'M', 'Q']:
            codes.append('LC' + b + a + CME.CME.value)
        for b in ['U', 'V', 'X', 'F', 'H', 'K', 'Q']:
            codes.append('FC' + b + a + CME.CME.value)
        for b in ['V', 'G', 'K', 'M', 'N', 'Q', 'V']:
            codes.append('LH' + b + a + CME.CME.value)
        for b in ['U', 'V', 'X', 'Z', 'F', 'G', 'H', 'K', 'M', 'N', 'Q']:
            codes.append('DA' + b + a + CME.CME.value)

    return codes


# DCE,CZC
def getDceCzc():
    codes = []
    list0 = ['98','99','00','01', '02', '03', '04', '05', '06', '07', '08','09','10','11','12','13','14','15','16', '17', '18', '19']
    list1 = ['6', '7', '8']
    list2 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    dce = ['M', 'Y', 'P', 'C', 'CS', 'JD', 'A']
    czc = ['RM', 'OI']

    # for a in dce:
    #     for b in list0:
    #         for c in list2:
    #             dcecodes = a + b + c + ".DCE"
    #             # codes.append(dcecodes)
    for a in czc:
        for b in list1:
            for c in list2:
                czccodes = a + b + c + ".CZC"
                codes.append(czccodes)
    #
    # for a in ["RO"]:
    #     for b in ['07','08','09','10','11','12','13','14']:
    #         for c in list2:
    #             czccodes = a + b + c + '.CZC'
    #             codes.append(czccodes)
    return codes


def getYueS():
    codes = []
    doupo = ['M01M.DCE', 'M03M.DCE', 'M05M.DCE', 'M07M.DCE', 'M08M.DCE', 'M09M.DCE', 'M11M.DCE', 'M12M.DCE']
    douyou = ['Y01M.DCE', 'Y03M.DCE', 'Y05M.DCE', 'Y07M.DCE', 'Y08M.DCE', 'Y09M.DCE', 'Y11M.DCE', 'Y12M.DCE']
    zonglvyou = ['P01M.DCE', 'P03M.DCE', 'P05M.DCE', 'P07M.DCE', 'P08M.DCE', 'P09M.DCE', 'P11M.DCE', 'P12M.DCE']

    caipo = ['RM01M.CZC', 'RM03M.CZC', 'RM05M.CZC', 'RM07M.CZC', 'RM08M.CZC', 'RM09M.CZC', 'RM11M.CZC']  # 没有12月的交易的东西
    caiyou = ['OI01M.CZC', 'OI03M.CZC', 'OI05M.CZC', 'OI07M.CZC', 'OI09M.CZC', 'OI11M.CZC']

    codes.extend(doupo)
    codes.extend(douyou)
    codes.extend(zonglvyou)
    codes.extend(caipo)
    codes.extend(caiyou)
    return codes


def getYueD():
    codes = []

    yumi = ['C01M.DCE', 'C03M.DCE', 'C05M.DCE', 'C07M.DCE', 'C09M.DCE', 'C11M.DCE']
    dianfen = ['CS01M.DCE', 'CS03M.DCE', 'CS05M.DCE', 'CS07M.DCE', 'CS09M.DCE', 'CS11M.DCE']
    jdan = ['JD01M.DCE', 'JD02M.DCE', 'JD03M.DCE', 'JD04M.DCE', 'JD05M.DCE', 'JD06M.DCE', 'JD07M.DCE', 'JD08M.DCE',
            'JD09M.DCE', 'JD10M.DCE', 'JD11M.DCE', 'JD12M.DCE']

    codes.extend(yumi)
    codes.extend(dianfen)
    codes.extend(jdan)

    return codes


# Others
others = ["USDCNY.IB", "USDX.FX", "EURUSD.FX", "USDCAD.FX", "USDJPY.FX", "GBPUSD.FX", "AUDUSD.FX", "BR.CME", "MP.CME",
          "CL.NYM", "CU.SHF", "SPTAUUSDOZ.IDC", "SPTAGUSDOZ.IDC", "IXIC.GI", "000001.SH", "SPX.GI", "FTSE.GI", "HSI.HI",
          "DJI.GI"]

if __name__ == "__main__":
    start_time = time.time()

    WindPy.w.start()

    codes = getCbotIce()
    # codes.extend(getCme())
    # codes.extend(getDceCzc())
    # codes.extend(others)

    codes = getDceCzc()

    failcodes = []
    threads = []
    codetype = False

    print(datetime.datetime.now())
    codes = list(chunks(codes, len(codes) // 1 + 1))

    for code in codes:
        th = threading.Thread(target=DataScrapy(code, codetype).run)
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    print('失败的代码为:', failcodes, '长度为', len(failcodes))
    end_time = time.time()

    print("程序运行所使用的时间为:", end_time - start_time)
