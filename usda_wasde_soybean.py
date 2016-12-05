from datetime import datetime

import xlrd
import usda_wasde_model

fileName = "wasde-12-10-2010.xls"

data = xlrd.open_workbook(fileName)

table = data.sheets()[8]

for i in range(table.nrows):
    recode = table.row_values(i)
    print(i, recode)

ddate = datetime.strptime(table.cell(1, 3).value, '%B %Y').date()

for i in (6, 7, 9):
    marketingYear = ''
    stage = ''
    if len(table.cell(6, i).value) > 7:
        temp = table.cell(6, i).value.split(" ")
        marketingYear = temp[0]
        stage = temp[1].rstrip('.')
    else:
        marketingYear = table.cell(6, i).value

    avgFarmPriceLow = 0.0
    avgFarmPriceHigh = 0.0
    if type(table.cell(25, i).value) == type(""):
        temp = table.cell(25, i).value.split(" - ")
        avgFarmPriceLow = float(temp[0])
        avgFarmPriceHigh = float(temp[1])
    else:
        avgFarmPriceLow = float(table.cell(25, i).value)
        avgFarmPriceHigh = float(table.cell(25, i).value)

    p = usda_wasde_model.usdaWasdeSoybean(
        PublicationDate=ddate,
        MarketingYear=marketingYear,  # 需要进行转化
        Stage=stage,  # 需要进行转化
        AreaPlanted=table.cell(10, i).value,
        AreaHarvested=table.cell(11, i).value,
        Yield=table.cell(13, i).value,
        BeginningStocks=table.cell(15, i).value,
        Production=table.cell(16, i).value,
        Imports=table.cell(17, i).value,
        TotalSupply=table.cell(18, i).value,
        Crushings=table.cell(19, i).value,
        Exports=table.cell(20, i).value,
        Seed=table.cell(21, i).value,
        Residual=table.cell(22, i).value,
        TotalUse=table.cell(23, i).value,
        EndingStocks=table.cell(24, i).value,
        AvgFarmPriceLow=avgFarmPriceLow,  # 需要进行转化
        AvgFarmPriceHigh=avgFarmPriceHigh,  # 需要进行转化
    )

    usda_wasde_model.session.add(p)
    # usda_wasde_model.session.commit()
    # try:
    #     usda_wasde_model.session.commit()
    # except:
    #     pass


    if type(table.cell(41, i).value) == type(""):
        temp = table.cell(41, i).value.split(" - ")
        avgFarmPriceLow = float(temp[0])
        avgFarmPriceHigh = float(temp[1])
    else:
        avgFarmPriceLow = float(table.cell(41, i).value)
        avgFarmPriceHigh = float(table.cell(41, i).value)
        
    p2 = usda_wasde_model.usdaWasdeSoybeanNoil(
        PublicationDate=ddate,
        MarketingYear=marketingYear,
        Stage=stage,
        BeginningStocks=table.cell(32, i).value,
        Production=table.cell(33, i).value,
        Imports=table.cell(34, i).value,
        TotalSupply=table.cell(35, i).value,
        DomesticDisappearance=table.cell(36, i).value,
        Biodiesel=table.cell(36, i).value,#
        FoodFeedIndustrial=table.cell(37, i).value,#
        Exports=table.cell(38, i).value,
        TotalUse=table.cell(39, i).value,
        EndingStocks=table.cell(40, i).value,
        AvgPriceLow=avgFarmPriceLow,
        AvgPriceHigh=avgFarmPriceHigh
    )
    # try:
    #     usda_wasde_model.session.add(p2)
    #     usda_wasde_model.session.commit()
    # except:
    #     pass

    # usda_wasde_model.session.add(p2)
    # usda_wasde_model.session.commit()


    if type(table.cell(56, i).value) == type(""):
        temp = table.cell(56, i).value.split(" - ")
        avgFarmPriceLow = float(temp[0])
        avgFarmPriceHigh = float(temp[1])
    else:
        avgFarmPriceLow = float(table.cell(56, i).value)
        avgFarmPriceHigh = float(table.cell(56, i).value)
    p3 = usda_wasde_model.usdaWasdeSoybeanMeal(
        PublicationDate=ddate,
        MarketingYear=marketingYear,
        Stage=stage,
        BeginningStocks=table.cell(48, i).value,
        Production=table.cell(49, i).value,
        Imports=table.cell(50, i).value,
        TotalSupply=table.cell(51, i).value,
        DomesticDisappearance=table.cell(52, i).value,
        Exports=table.cell(53, i).value,
        TotalUse=table.cell(54, i).value,
        EndingStocks=table.cell(55, i).value,
        AvgPriceLow=avgFarmPriceLow,
        AvgPriceHigh=avgFarmPriceHigh,
    )
    usda_wasde_model.session.add(p3)


usda_wasde_model.session.commit()