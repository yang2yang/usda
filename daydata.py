import WindPy
import pymysql
import datetime
import time
import threading
from enum import Enum


# 切分list 利用的是生成器生成
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class DataScrapy:
    # name是线程的名字，codes表示需要抓取的code条码，codetype表示是否是分钟数据，tablename表示操作哪一张表
    def __init__(self, codes, codetype, tablename):
        self.tablename = tablename
        self.codetype = codetype
        self.flag = "open,high,low,close,volume,amt,chg,pct_chg,oi"
        # self.flag1 ="pre_close,open,high,low,close,volume,amt,dealnum,chg,pct_chg,swing,vwap,oi,oi_chg,pre_settle,settle,chg_settlement,pct_chg_settlement,lastradeday_s,last_trade_day"
        self.codes = codes
        self.deltadays1 = datetime.timedelta(days=1)
        self.today = datetime.date.today() + self.deltadays1  # 获取今天日期
        self.deltadays = datetime.timedelta(days=4)  # 确定日期差额，如前天 days=2
        self.yesterday = self.today - self.deltadays  # 获取差额日期，昨天

    # 获得数据库的连接和cursor
    def getConnCursor(self):
        self.db = pymysql.connect("192.168.5.12", "root", "root123", "data_analyze")
        self.cursor = self.db.cursor()

    # 保存数据到数据库中 TODO:待优化 分割功能块
    def saveData(self, outdata, code):
        if outdata.ErrorCode != 0:
            failcodes.append([code, outdata.ErrorCode])
            return ()
        for i in range(0, len(outdata.Data[0])):
            datalist = []
            datalist.append('"' + str(outdata.Codes[0]) + '"')
            if len(outdata.Times) > 0:
                dt = '"' + str(outdata.Times[i])[0:-7] + '"'
                dt_sql = dt[1:5]
                datalist.append(dt)
            for k in range(0, len(outdata.Fields)):
                if (k != 7):
                    datalist.append(str(outdata.Data[k][i]))
                else:
                    datalist.append(str(outdata.Data[k][i])[:9])

            temp = ','.join(datalist)

            # promise after 4 open is not 0 then insert into the mysql
            if int(100 * outdata.Data[0][i]) != 0 and int(100 * outdata.Data[1][i]) != 0 and int(
                            100 * outdata.Data[2][i]) != 0 and int(100 * outdata.Data[3][i]) != 0:
                # print('看一下4个都有数的情况下  ','len(result)=',len(result))
                # TODO把数据库给抽象出来，减少sql语句的耦合度
                sql = 'insert into ' + self.tablename + ' values(' + temp + ');'
                print(sql)
                try:
                    self.cursor.execute(sql)
                    self.db.commit()
                except:
                    print("该条数据已插入到数据库中")
                    self.db.rollback()
            else:
                print('数据不完整不插入数据库中')

    # 线程中被运行的run方法
    def run(self):

        self.getConnCursor()
        if self.codetype == False:
            for code in self.codes:
                self.saveData(WindPy.w.wsd(code, self.flag, str(self.yesterday), str(self.today), "", showblank=0),
                              code)
            # self.db.close()
        # else:
        #     for code in self.codes:
        #         if code in codeYS:
        #             self.saveData(WindPy.w.wsi(code, self.flag, str(self.yesterday), str(self.today),
        #                                        "periodstart=09:00:00;periodend=10:15:00", showblank=0), code)
        #             self.saveData(WindPy.w.wsi(code, self.flag, str(self.yesterday), str(self.today),
        #                                        "periodstart=10:30:00;periodend=11:30:00", showblank=0), code)
        #             self.saveData(WindPy.w.wsi(code, self.flag, str(self.yesterday), str(self.today),
        #                                        "periodstart=13:30:00;periodend=15:00:00", showblank=0), code)
        #             self.saveData(WindPy.w.wsi(code, self.flag, str(self.yesterday), str(self.today),
        #                                        "periodstart=21:00:00;periodend=23:30:00", showblank=0), code)
        #         if code in codeYD:
        #             self.saveData(WindPy.w.wsi(code, self.flag, str(self.yesterday), str(self.today),
        #                                        "periodstart=09:00:00;periodend=10:15:00", showblank=0), code)
        #             self.saveData(WindPy.w.wsi(code, self.flag, str(self.yesterday), str(self.today),
        #                                        "periodstart=10:30:00;periodend=11:30:00", showblank=0), code)
        #             self.saveData(WindPy.w.wsi(code, self.flag, str(self.yesterday), str(self.today),
        #                                        "periodstart=13:30:00;periodend=15:00:00", showblank=0), code)
        #     self.db.close()


# CBOT,ICE
def getCbotIce():
    codes = []
    # 年份表示90年到23年的合约
    list0 = ['16', '17', '18', '19']
    # 国外的月份时间表示
    list4 = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z']

    # 国外ICE和CME，另外代码中都是有E的
    cbt = ['S', 'C', 'BO', 'SM', 'ZE', 'W', 'RR', 'O']
    nice = ['SB', 'KC', 'CT', 'CC', 'DX']

    for a in nice:
        for b in list4:
            for c in list0:
                icecodes = a + b + c + "E" + ".NYB"
                codes.append(icecodes)
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
    list0 = ['16', '17', '18', '19']
    list1 = ['6', '7', '8']
    list2 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    dce = ['M', 'Y', 'P', 'C', 'CS', 'JD']
    czc = ['RM', 'OI']

    for a in dce:
        for b in list0:
            for c in list2:
                dcecodes = a + b + c + ".DCE"
                codes.append(dcecodes)
    for a in czc:
        for b in list1:
            for c in list2:
                czccodes = a + b + c + ".CZC"
                codes.append(czccodes)
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
    codes.extend(getCme())
    codes.extend(getDceCzc())
    codes.extend(others)

    failcodes = []
    threads = []
    codetype = False

    print(datetime.datetime.now())
    codes = list(chunks(codes, len(codes) // 30 + 1))

    for code in codes:
        th = threading.Thread(target=DataScrapy(code, codetype, "daydata_echart").run)
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    codetype = True
    threads = []
    failcodes = []
    codes = []

    codeYS = getYueS()
    codeYD = getYueD()
    codes.extend(codeYS)
    codes.extend(codeYD)
    codes = list(chunks(codes, len(codes) // 30 + 1))

    for code in codes:
        th = threading.Thread(target=DataScrapy(code, codetype, "mdata").run)
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    print('失败的代码为:', failcodes, '长度为', len(failcodes))
    end_time = time.time()

    print("程序运行所使用的时间为:", end_time - start_time)
