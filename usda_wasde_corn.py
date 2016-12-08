from datetime import datetime
import os
import xlrd
import usda_wasde_model

filePath = "10s/2010/"
fileName = filePath + "wasde-01-12-2016.xls"
for d in os.listdir(filePath):
# for d in ['wasde-12-09-2015.xls']:
    data = xlrd.open_workbook(filePath+d)

    table = data.sheet_by_name('Page 12')

    for i in range(table.nrows):
        recode = table.row_values(i)
        print(i, recode)

    datex = 0
    datey = 0

    datex = 1
    datey = 2

    ddate = datetime.strptime(table.cell(datex, datey).value, '%B %Y').date()


    # 需要进行部分转化
    def getCell(x, y):
        if x is not None:
            v = table.cell(x, y).value
            if v == 'NA':
                return None
            if type(v) == type(""):
                if "*" in v:
                    return float(v.rstrip('*').rstrip(" "))
                if "/" in v:
                    return float(v.split(" ")[0].replace(",", ""))
            return v
        else:
            return None


    def parseMarketAndYear(x, y):
        if len(table.cell(x, y).value) > 7:
            temp = table.cell(x, y).value.split(" ")
            marketingYear = temp[0]
            stage = temp[1].rstrip('.')
        else:
            marketingYear = table.cell(x, y).value
            stage = ''
        return marketingYear, stage


    def isEquall(v1, v2):
        if v1 != '' and v2 != '':
            return (v1.replace(" ", '').upper() in v2.replace(" ", '').upper()) or (
                v2.replace(" ", '').upper() in v1.replace(" ", '').upper())
        else:
            return False


    def getByTitle(startx, starty, title, endx):
        for i in range(startx, endx):
            # 找到的第一个
            if isEquall(table.cell(i, starty).value, title):
                return i


    def getAllTitle(xxpoint, yypoint, endx):
        areaPlanted = getByTitle(startx=xxpoint, starty=yypoint, title="Area Planted", endx=endx)
        areaHarvested = getByTitle(startx=xxpoint, starty=yypoint, title="Area Harvested", endx=endx)
        yYield = getByTitle(startx=xxpoint, starty=yypoint, title="Yield per Harvested Acre", endx=endx)
        beginningStocks = getByTitle(startx=xxpoint, starty=yypoint, title="Beginning Stocks", endx=endx)
        production = getByTitle(startx=xxpoint, starty=yypoint, title="Production", endx=endx)
        imports = getByTitle(startx=xxpoint, starty=yypoint, title="Imports", endx=endx)
        TotalSupply = getByTitle(startx=xxpoint, starty=yypoint, title="    Supply, Total", endx=endx)
        FeedandResidual = getByTitle(startx=xxpoint, starty=yypoint, title="Feed and Residual", endx=endx)
        FoodSeedIndustrial = getByTitle(startx=xxpoint, starty=yypoint, title="Food, Seed & Industrial", endx=endx)
        EthanolByProducts = getByTitle(startx=xxpoint, starty=yypoint, title="Ethanol & by-products", endx=endx)
        TotalDomestic = getByTitle(startx=xxpoint, starty=yypoint, title="Domestic, Total", endx=endx)
        exports = getByTitle(startx=xxpoint, starty=yypoint, title="Exports", endx=endx)
        totalUse = getByTitle(startx=xxpoint, starty=yypoint, title="    Use, Total", endx=endx)
        endingStocks = getByTitle(startx=xxpoint, starty=yypoint, title="Ending Stocks", endx=endx)

        allTitle = {}
        allTitle["Area Planted"] = areaPlanted
        allTitle["Area Harvested"] = areaHarvested
        allTitle["Yield per Harvested Acre"] = yYield
        allTitle["Beginning Stocks"] = beginningStocks
        allTitle["Production"] = production
        allTitle["Imports"] = imports
        allTitle["    Supply, Total"] = TotalSupply
        allTitle["Feed and Residual"] = FeedandResidual
        allTitle["Food, Seed & Industrial"] = FoodSeedIndustrial
        allTitle["Ethanol & by-products"] = EthanolByProducts
        allTitle["Domestic, Total"] = TotalDomestic
        allTitle["Exports"] = exports
        allTitle["    Use, Total"] = totalUse
        allTitle["Ending Stocks"] = endingStocks
        return allTitle;


    def getHighLow(xxpoint, yypoint, i, name, endx):
        avgFarmPrice = getByTitle(startx=xxpoint, starty=yypoint, title=name, endx=endx)
        if type(table.cell(avgFarmPrice, i).value) == type(""):
            temp = table.cell(avgFarmPrice, i).value.split(" - ")
            avgFarmPriceLow = float(temp[0])
            avgFarmPriceHigh = float(temp[1])
        else:
            avgFarmPriceLow = float(table.cell(avgFarmPrice, i).value)
            avgFarmPriceHigh = float(table.cell(avgFarmPrice, i).value)
        return avgFarmPriceLow, avgFarmPriceHigh


    base = 1
    base = 3
    xxpoint = 31
    yypoint = 2

    # xxpoint = 31
    # yypoint = 0
    marketLine = 8

    marketLine = 7
    for i in (base, base + 1, base + 3):
        marketingYear, stage = parseMarketAndYear(marketLine, i)

        allTitle = getAllTitle(xxpoint, yypoint, table.nrows)
        avgFarmPriceLow, avgFarmPriceHigh = getHighLow(xxpoint, yypoint, i, "Avg", table.nrows)

        p = usda_wasde_model.UsdaWasdeCorn(
            PublicationDate=ddate,
            MarketingYear=marketingYear,
            Stage=stage,
            AreaPlanted=getCell(allTitle["Area Planted"], i),
            AreaHarvested=getCell(allTitle["Area Harvested"], i),
            Yield=getCell(allTitle["Yield per Harvested Acre"], i),
            BeginningStocks=getCell(allTitle["Beginning Stocks"], i),
            Production=getCell(allTitle["Production"], i),
            Imports=getCell(allTitle["Imports"], i),
            TotalSupply=getCell(allTitle["    Supply, Total"], i),
            FeedandResidual=getCell(allTitle["Feed and Residual"], i),
            FoodSeedIndustrial=getCell(allTitle["Food, Seed & Industrial"], i),
            EthanolByProducts=getCell(allTitle["Ethanol & by-products"], i),
            TotalDomestic=getCell(allTitle["Domestic, Total"], i),
            Exports=getCell(allTitle["Exports"], i),
            TotalUse=getCell(allTitle["    Use, Total"], i),
            EndingStocks=getCell(allTitle["Ending Stocks"], i),
            AvgFarmPriceLow=avgFarmPriceLow,
            AvgFarmPriceHigh=avgFarmPriceHigh,
        )
        usda_wasde_model.session.add(p)

    usda_wasde_model.session.commit()
