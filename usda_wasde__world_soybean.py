from datetime import datetime

import xlrd
import usda_wasde_model

fileName = "wasde-12-10-2010.xls"

data = xlrd.open_workbook(fileName)

table = data.sheet_by_name('Page 28')

for i in range(table.nrows):
    recode = table.row_values(i)
    print(i, recode)

ddate = datetime.strptime(table.cell(1, 1).value, '%B %Y').date()

for i in range(11,22):
    p = usda_wasde_model.usdaWasdeWorldSoybean(
        PublicationDate=ddate,
        MarketingYear=table.cell(9,1).value,
        Stage='',
        Country=table.cell(i,1).value,
        BeginningStocks=table.cell(i,6).value,
        Production=table.cell(i,7).value,
        Imports=table.cell(i,8).value,
        DomesticFeed=table.cell(i,9).value,
        TotalDomestic=table.cell(i,10).value,
        Exports=table.cell(i,i).value,
        EndingStocks=table.cell(i,12).value
    )
    usda_wasde_model.session.add(p)

for i in range(26,37):
    p = usda_wasde_model.usdaWasdeWorldSoybean(
        PublicationDate=ddate,
        MarketingYear=table.cell(24,1).value,
        Stage='',
        Country=table.cell(i,1).value,
        BeginningStocks=table.cell(i,6).value,
        Production=table.cell(i,7).value,
        Imports=table.cell(i,8).value,
        DomesticFeed=table.cell(i,9).value,
        TotalDomestic=table.cell(i,10).value,
        Exports=table.cell(i,i).value,
        EndingStocks=table.cell(i,12).value
    )
    usda_wasde_model.session.add(p)


for i in range(42,64):
    p = usda_wasde_model.usdaWasdeWorldSoybean(
        PublicationDate=ddate,
        MarketingYear=table.cell(40,1).value,
        Stage='',
        Country=table.cell(i,1).value,
        BeginningStocks=table.cell(i,6).value,
        Production=table.cell(i,7).value,
        Imports=table.cell(i,8).value,
        DomesticFeed=table.cell(i,9).value,
        TotalDomestic=table.cell(i,10).value,
        Exports=table.cell(i,i).value,
        EndingStocks=table.cell(i,12).value
    )
    usda_wasde_model.session.add(p)

usda_wasde_model.session.commit()