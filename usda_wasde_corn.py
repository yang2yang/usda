from datetime import datetime

import xlrd
import usda_wasde_model

fileName = "wasde-12-10-2010.xls"

data = xlrd.open_workbook(fileName)

table = data.sheet_by_name('Page 12')

for i in range(table.nrows):
    recode = table.row_values(i)
    print(i,recode)


ddate = datetime.strptime(table.cell(1,2).value,'%B %Y').date()
for i in (3, 4, 6):
    marketingYear = ''
    stage = ''
    if len(table.cell(7, i).value) > 7:
        temp = table.cell(7, i).value.split(" ")
        marketingYear = temp[0]
        stage = temp[1].rstrip('.')
    else:
        marketingYear = table.cell(7, i).value

    avgFarmPriceLow = 0.0
    avgFarmPriceHigh = 0.0
    if type(table.cell(53, i).value) == type(""):
        temp = table.cell(53, i).value.split(" - ")
        avgFarmPriceLow = float(temp[0])
        avgFarmPriceHigh = float(temp[1])
    else:
        avgFarmPriceLow = float(table.cell(53, i).value)
        avgFarmPriceHigh = float(table.cell(53, i).value)

    p = usda_wasde_model.UsdaWasdeCorn(
    PublicationDate=ddate,
    MarketingYear=marketingYear,
    Stage=stage,
    AreaPlanted=table.cell(34,i).value,
    AreaHarvested=table.cell(35,i).value,
    Yield=table.cell(37,i).value,
    BeginningStocks=table.cell(39,i).value,
    Production=table.cell(40,i).value,
    Imports=table.cell(41,i).value,
    TotalSupply=table.cell(42,i).value,
    FeedandResidual=table.cell(43,i).value,
    FoodSeedIndustrial=table.cell(44,i).value,
    EthanolByProducts=table.cell(45,i).value,
    TotalDomestic=table.cell(46,i).value,
    Exports=table.cell(47,i).value,
    TotalUse=table.cell(48,i).value,
    EndingStocks=table.cell(49,i).value,
    AvgFarmPriceLow=table.cell(50,i).value,
    AvgFarmPriceHigh=table.cell(51,i).value,
    )
    usda_wasde_model.session.add(p)

usda_wasde_model.session.commit()