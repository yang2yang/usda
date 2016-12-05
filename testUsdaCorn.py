import xlrd
import usda_wasde_model

fileName = "USDA-SB.xlsx"


data = xlrd.open_workbook(fileName)

table = data.sheets()[0]

for i in range(2,table.nrows):
    recode = table.row_values(i)

    print(recode)

    for j in range(len(recode)):
        if recode[j] == '':
            recode[j] = None

    if recode[2] is not None:
        recode[2] = xlrd.xldate.xldate_as_datetime(recode[2], 0)

    p = usda_wasde_model.UsdaWasdeCorn(
        PublicationDate=recode[2],
        MarketingYear=recode[0],
        Stage=recode[1],
        AreaPlanted=recode[5],
        AreaHarvested=recode[6],
        Yield=recode[7],
        BeginningStocks=recode[9],#期初库存
        Production=recode[10],#产量
        Imports=recode[11],
        TotalSupply=recode[12],#总供给
        FeedandResidual=recode[],
        FoodSeedIndustrial=recode[],
        EthanolByProducts=recode[],
        TotalDomestic=recode[],
        Exports=recode[14],
        TotalUse=recode[16],
        EndingStocks=recode[17],
        AvgFarmPriceLow=recode[18],
        AvgFarmPriceHigh=recode[19]
    )
    usda_wasde_model.session.add(p)

usda_wasde_model.session.commit()