from datetime import datetime
import os
import xlrd
import usda_wasde_model as usda

filePath = '10s/2010/'
# fileName = 'wasde-11-09-2016.xls'
for d in os.listdir(filePath):
# for d in ['wasde-12-09-2015.xls']:
    data = xlrd.open_workbook(filePath + d)
    table = data.sheet_by_name('Page 23')

    for i in range(table.nrows):
        recode = table.row_values(i)
        print(i, recode)


    def parseMarketAndYear(x, y):
        if len(table.cell(x, y).value) > 7:
            temp = table.cell(x, y).value.split(" ")
            marketingYear = temp[0]
            stage = temp[1].rstrip('.')
        else:
            marketingYear = table.cell(x, y).value
            stage = ''
        return marketingYear, stage


    # datex, datey = 0, 0
    datex, datey = 2, 2
    ddate = datetime.strptime(table.cell(datex, datey).value, '%B %Y').date()

    # marketingYear的起始位置
    x, y = 10, 3
    # x, y = 8, 0
    # marketingYear到真正数据的间隔 marketingYear + offset = 真正数据的位置
    offset = 2

    marketingYear, stage = parseMarketAndYear(x, y)
    offset2 = 0
    offset2 = 2

    for i in range(x + offset, table.nrows - 1):
        if 'Selected Other' in table.cell(i, y).value or table.cell(i, y).value == '':
            continue

        p = usda.usdaWasdeWorldCorn(
            PublicationDate=ddate,
            MarketingYear=marketingYear,
            Stage=stage,
            Country=table.cell(i, y).value,
            # 取第二行的数据
            BeginningStocks=table.cell(i + 1, y + offset2 + 2).value,
            Production=table.cell(i + 1, y + offset2 + 3).value,
            Imports=table.cell(i + 1, y + offset2 + 4).value,
            DomesticCrush=table.cell(i + 1, y + offset2 + 5).value,
            TotalDomestic=table.cell(i + 1, y + offset2 + 6).value,
            Exports=table.cell(i + 1, y + offset2 + 7).value,
            EndingStocks=table.cell(i + 1, y + offset2 + 8).value,
        )
        print("BeginningStocks=", table.cell(i + 1, y + offset2 + 2).value)
        usda.session.add(p)

    usda.session.commit()
