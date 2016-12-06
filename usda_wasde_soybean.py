from datetime import datetime

import xlrd
import usda_wasde_model

fileName = "10s/2016/wasde-09-12-2016.xls"
fileName = "10s/2010/wasde-07-09-2010.xls"

data = xlrd.open_workbook(fileName)

table = data.sheet_by_name('Page 15')

for i in range(table.nrows):
    recode = table.row_values(i)
    print(i, recode)

# 相对位置是一定的  输入两个东西一个是时间，一个是第一张表格的左上角的东西
# xpoint = 0
# ypoint = 0
#
# xxpoint = 8
# yypoint = 0
#
# xpoint2 = 33
# ypoint2 = 0
#
# xpoint3 = 45
# ypoint3 = 0

xpoint = 1
ypoint = 3

xxpoint = 6
yypoint = 2

xpoint2 = 28
ypoint2 = 2

xpoint3 = 45
ypoint3 = 2

ddate = datetime.strptime(table.cell(xpoint, ypoint).value, '%B %Y').date()


def isEquall(v1, v2):
    if v1 != '' and v2 != '':
        return (v1.replace(" ", '').upper() in v2.replace(" ", '').upper()) or (v2.replace(" ", '').upper() in v1.replace(" ", '').upper())
    else:
        return False

def getByTitle(startx, starty, title, endx):
    for i in range(startx, endx):
        # 找到的第一个
        if isEquall(table.cell(i, starty).value, title):
            return i


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
                return float(v.split(" ")[0].replace(",",""))
    else:
        return None

def getAllTitle(xxpoint, yypoint, endx):
    areaPlanted = getByTitle(startx=xxpoint, starty=yypoint, title="Area Planted", endx=endx)
    areaHarvested = getByTitle(startx=xxpoint, starty=yypoint, title="Area Harvested", endx=endx)
    yYield = getByTitle(startx=xxpoint, starty=yypoint, title="Yield per Harvested Acre", endx=endx)
    beginningStocks = getByTitle(startx=xxpoint, starty=yypoint, title="Beginning Stocks", endx=endx)
    production = getByTitle(startx=xxpoint, starty=yypoint, title="Production", endx=endx)
    imports = getByTitle(startx=xxpoint, starty=yypoint, title="Imports", endx=endx)
    totalSupply = getByTitle(startx=xxpoint, starty=yypoint, title="    Supply, Total", endx=endx)
    crushings = getByTitle(startx=xxpoint, starty=yypoint, title="Crushings", endx=endx)
    exports = getByTitle(startx=xxpoint, starty=yypoint, title="Exports", endx=endx)
    seed = getByTitle(startx=xxpoint, starty=yypoint, title="Seed", endx=endx)
    residual = getByTitle(startx=xxpoint, starty=yypoint, title="Residual", endx=endx)
    totalUse = getByTitle(startx=xxpoint, starty=yypoint, title="    Use, Total", endx=endx)
    endingStocks = getByTitle(startx=xxpoint, starty=yypoint, title="Ending Stocks", endx=endx)

    allTitle = {}
    allTitle["Area Planted"] = areaPlanted
    allTitle["Area Harvested"] = areaHarvested
    allTitle["Yield per Harvested Acre"] = yYield
    allTitle["Beginning Stocks"] = beginningStocks
    allTitle["Production"] = production
    allTitle["Imports"] = imports
    allTitle["    Supply, Total"] = totalSupply
    allTitle["Crushings"] = crushings
    allTitle["Exports"] = exports
    allTitle["Seed"] = seed
    allTitle["Residual"] = residual
    allTitle["    Use, Total"] = totalUse
    allTitle["Ending Stocks"] = endingStocks
    return allTitle;


def getAllTitle2(xxpoint, yypoint, endx):
    beginningStocks = getByTitle(startx=xxpoint, starty=yypoint, title="Beginning Stocks", endx=endx)
    production = getByTitle(startx=xxpoint, starty=yypoint, title="Production", endx=endx)
    imports = getByTitle(startx=xxpoint, starty=yypoint, title="Imports", endx=endx)
    totalSupply = getByTitle(startx=xxpoint, starty=yypoint, title="    Supply, Total", endx=endx)
    DomesticDisappearance = getByTitle(startx=xxpoint, starty=yypoint, title="Domestic Disappearance", endx=endx)
    Biodiesel = getByTitle(startx=xxpoint, starty=yypoint, title="     Biodiesel", endx=endx)
    FoodFeedIndustrial = getByTitle(startx=xxpoint, starty=yypoint, title="     Food, Feed & other Industrial",
                                    endx=endx)
    exports = getByTitle(startx=xxpoint, starty=yypoint, title="Exports", endx=endx)
    totalUse = getByTitle(startx=xxpoint, starty=yypoint, title="    Use, Total", endx=endx)
    endingStocks = getByTitle(startx=xxpoint, starty=yypoint, title="Ending Stocks", endx=endx)

    allTitle = {}
    allTitle["Beginning Stocks"] = beginningStocks
    allTitle["Production 4/"] = production
    allTitle["Imports"] = imports
    allTitle["    Supply, Total"] = totalSupply
    allTitle["Domestic Disappearance"] = DomesticDisappearance
    allTitle["     Biodiesel 3/"] = Biodiesel
    allTitle["     Food, Feed & other Industrial"] = FoodFeedIndustrial
    allTitle["Exports"] = exports
    allTitle["    Use, Total"] = totalUse
    allTitle["Ending Stocks"] = endingStocks
    return allTitle;


def getAllTitle3(xxpoint, yypoint, endx):
    beginningStocks = getByTitle(startx=xxpoint, starty=yypoint, title="Beginning Stocks", endx=endx)
    production = getByTitle(startx=xxpoint, starty=yypoint, title="Production", endx=endx)
    imports = getByTitle(startx=xxpoint, starty=yypoint, title="Imports", endx=endx)
    totalSupply = getByTitle(startx=xxpoint, starty=yypoint, title="    Supply, Total", endx=endx)
    DomesticDisappearance = getByTitle(startx=xxpoint, starty=yypoint, title="Domestic Disappearance", endx=endx)
    exports = getByTitle(startx=xxpoint, starty=yypoint, title="Exports", endx=endx)
    totalUse = getByTitle(startx=xxpoint, starty=yypoint, title="    Use, Total", endx=endx)
    endingStocks = getByTitle(startx=xxpoint, starty=yypoint, title="Ending Stocks", endx=endx)

    allTitle = {}
    allTitle["Beginning Stocks"] = beginningStocks
    allTitle["Production 4/"] = production
    allTitle["Imports"] = imports
    allTitle["    Supply, Total"] = totalSupply
    allTitle["Domestic Disappearance"] = DomesticDisappearance
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


# 需要取出来的1,2,4列
for i in (yypoint + 4, yypoint + 5, yypoint + 7):
    marketingYear = ''
    stage = ''
    if len(table.cell(xxpoint, i).value) > 7:
        temp = table.cell(xxpoint, i).value.split(" ")
        marketingYear = temp[0]
        stage = temp[1].rstrip('.')
    else:
        marketingYear = table.cell(xxpoint, i).value

    avgFarmPriceLow, avgFarmPriceHigh = getHighLow(xxpoint, yypoint, i, "Avg", xpoint2)

    allTitle = getAllTitle(xxpoint, yypoint, xpoint2)

    p = usda_wasde_model.usdaWasdeSoybean(
        PublicationDate=ddate,
        MarketingYear=marketingYear,  # 需要进行转化
        Stage=stage,  # 需要进行转化
        AreaPlanted=getCell(allTitle["Area Planted"], i),
        AreaHarvested=getCell(allTitle["Area Harvested"], i),
        Yield=getCell(allTitle["Yield per Harvested Acre"], i),
        BeginningStocks=getCell(allTitle["Beginning Stocks"], i),
        Production=getCell(allTitle["Production"], i),
        Imports=getCell(allTitle["Imports"], i),
        TotalSupply=getCell(allTitle["    Supply, Total"], i),
        Crushings=getCell(allTitle["Crushings"], i),
        Exports=getCell(allTitle["Exports"], i),
        Seed=getCell(allTitle["Seed"], i),
        Residual=getCell(allTitle["Residual"], i),
        TotalUse=getCell(allTitle["    Use, Total"], i),
        EndingStocks=getCell(allTitle["Ending Stocks"], i),
        AvgFarmPriceLow=avgFarmPriceLow,  # 需要进行转化
        AvgFarmPriceHigh=avgFarmPriceHigh,  # 需要进行转化
    )

    usda_wasde_model.session.add(p)

    avgFarmPriceLow, avgFarmPriceHigh = getHighLow(xpoint2, ypoint2, i, "Avg", xpoint3)
    allTitle = getAllTitle2(xpoint2, ypoint2, xpoint3)


    p2 = usda_wasde_model.usdaWasdeSoybeanNoil(
        PublicationDate=ddate,
        MarketingYear=marketingYear,
        Stage=stage,
        BeginningStocks=getCell(allTitle["Beginning Stocks"], i),
        Production=getCell(allTitle["Production 4/"], i),
        Imports=getCell(allTitle["Imports"], i),
        TotalSupply=getCell(allTitle["    Supply, Total"], i),
        DomesticDisappearance=getCell(allTitle["Domestic Disappearance"], i),
        Biodiesel=getCell(allTitle["     Biodiesel 3/"], i),
        FoodFeedIndustrial=getCell(allTitle["     Food, Feed & other Industrial"], i),
        Exports=getCell(allTitle["Exports"], i),
        TotalUse=getCell(allTitle["    Use, Total"], i),
        EndingStocks=getCell(allTitle["Ending Stocks"], i),
        AvgPriceLow=avgFarmPriceLow,
        AvgPriceHigh=avgFarmPriceHigh
    )
    usda_wasde_model.session.add(p2)



    avgFarmPriceLow, avgFarmPriceHigh = getHighLow(xpoint3, ypoint3, i, "Avg", table.nrows)
    allTitle = getAllTitle3(xpoint3, ypoint3, table.nrows)

    p3 = usda_wasde_model.usdaWasdeSoybeanMeal(
        PublicationDate=ddate,
        MarketingYear=marketingYear,
        Stage=stage,
        BeginningStocks=getCell(allTitle["Beginning Stocks"], i),
        Production=getCell(allTitle["Production 4/"], i),
        Imports=getCell(allTitle["Imports"], i),
        TotalSupply=getCell(allTitle["    Supply, Total"], i),
        DomesticDisappearance=getCell(allTitle["Domestic Disappearance"], i),
        Exports=getCell(allTitle["Exports"], i),
        TotalUse=getCell(allTitle["    Use, Total"], i),
        EndingStocks=getCell(allTitle["Ending Stocks"], i),
        AvgPriceLow=avgFarmPriceLow,
        AvgPriceHigh=avgFarmPriceHigh,
    )
    usda_wasde_model.session.add(p3)

usda_wasde_model.session.commit()
