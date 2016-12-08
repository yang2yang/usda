from datetime import datetime
import os
import xlrd
import usda_wasde_model

fileName = "10s//2016/wasde-11-09-2016.xls"
dirname = "10s/2013/"

for d in os.listdir(dirname):
    print(d)
    data = xlrd.open_workbook(dirname + d)

    table = data.sheet_by_name('Page 28')

    for i in range(table.nrows):
        recode = table.row_values(i)
        print(i, recode)

    # country和BeginningStocks之间有多少空字符串
    offset = 1
    datex = 0
    datey = 0

    datex = 1
    datey = 1

    ddate = datetime.strptime(table.cell(datex, datey).value, '%B %Y').date()

    def parseMarketAndStage(x, y):
        if len(table.cell(x, y).value) > 7:
            temp = table.cell(x, y).value.split(" ")
            marketingYear = temp[0]
            stage = temp[1].rstrip('.')
        else:
            marketingYear = table.cell(x, y).value
            stage = ''
        return marketingYear, stage


    x1 = 8
    y1 = 0

    x1 = 9
    y1 = 1

    marketingYear, stage = parseMarketAndStage(x1, y1)

    x1 += x1
    offset = 5

    for i in range(x1 + 1, x1 + 15):
        # 直到空行结束
        if table.cell(i, offset + 1).value == '':
            break
        p = usda_wasde_model.usdaWasdeWorldSoybean(
            PublicationDate=ddate,
            MarketingYear=marketingYear,
            Stage=stage,
            Country=table.cell(i, y1).value,
            BeginningStocks=table.cell(i, offset + 1).value,
            Production=table.cell(i, offset + 2).value,
            Imports=table.cell(i, offset + 3).value,
            DomesticFeed=table.cell(i, offset + 4).value,
            TotalDomestic=table.cell(i, offset + 5).value,
            Exports=table.cell(i, offset + 6).value,
            EndingStocks=table.cell(i, offset + 7).value
        )
        usda_wasde_model.session.add(p)

    x2 = 24
    y2 = 0

    x2 = 25
    y2 = 1

    x2 = 24
    y2 = 1
    marketingYear, stage = parseMarketAndStage(x2, y2)

    x2 += 1

    for i in range(x2 + 1, x2 + 15):
        if table.cell(i, offset + 1).value == '':
            break
        p = usda_wasde_model.usdaWasdeWorldSoybean(
            PublicationDate=ddate,
            MarketingYear=marketingYear,
            Stage=stage,
            Country=table.cell(i, y2).value,
            BeginningStocks=table.cell(i, offset + 1).value,
            Production=table.cell(i, offset + 2).value,
            Imports=table.cell(i, offset + 3).value,
            DomesticFeed=table.cell(i, offset + 4).value,
            TotalDomestic=table.cell(i, offset + 5).value,
            Exports=table.cell(i, offset + 6).value,
            EndingStocks=table.cell(i, offset + 7).value
        )
        usda_wasde_model.session.add(p)

    x3 = 40
    y3 = 0

    x3 = 42
    y3 = 1

    x3 = 40
    y3 = 1
    marketingYear, stage = parseMarketAndStage(x3, y3)

    x3 += 1
    for i in range(x3 + 1, x3 + 25,2):
        if table.cell(i+1,offset+3).value == '':
            break
        p = usda_wasde_model.usdaWasdeWorldSoybean(
            PublicationDate=ddate,
            MarketingYear=marketingYear,
            Stage=stage,
            Country=table.cell(i, y3).value,
            BeginningStocks=table.cell(i+1, offset + 1).value,
            Production=table.cell(i+1, offset + 2).value,
            Imports=table.cell(i+1, offset + 3).value,
            DomesticFeed=table.cell(i+1, offset + 4).value,
            TotalDomestic=table.cell(i+1, offset + 5).value,
            Exports=table.cell(i+1, offset + 6).value,
            EndingStocks=table.cell(i+1, offset + 7).value
        )
        usda_wasde_model.session.add(p)

    usda_wasde_model.session.commit()
