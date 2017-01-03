import xlrd
import spotgoods.spotgoodsmodel as sgm

fileName = "spotgoodsdata/油脂品种(1).xlsx"
fileName = "spotgoodsdata/油料品种(1).xlsx"

data = xlrd.open_workbook(fileName)

# table = data.sheet_by_name("国产蛋白豆粕价格")
table = data.sheet_by_name("国内菜籽粕价格")
# table = data.sheet_by_name("油脂处理")

for i in range(table.nrows):
    recode = table.row_values(i)
    print(i, recode)


def getRegion(col):
    return table.cell(3, col).value


def getDate(row):
    return xlrd.xldate.xldate_as_datetime(table.cell(row, 0).value, 0)


def getPrice(i, j):
    #  必须有一个值
    if table.cell(i, j).value == '':
        return None
    return table.cell(i, j).value


def getStateByRegion(commodity, region):
    p = sgm.session.query(sgm.StateRegion).filter_by(agri_type=commodity, agri_region=region).first()
    return p.agri_state

# 油料从第5行开始循环
for i in range(5, table.nrows):
    # 从第2列开始
    for j in range(2, 24 ):
        if getPrice(i,j) is not None:
            p = sgm.SpotMarketChina(Commodity="普通菜籽粕", Date=getDate(i), State=getStateByRegion("菜粕", getRegion(j)),
                                    Region=getRegion(j),
                                    Price=getPrice(i,j))
            sgm.session.add(p)
            try:
                sgm.session.commit()
            except:
                pass
            sgm.session.close()





# 油脂从第2行开始循环
# for i in range(2, table.nrows):
#     # 从第2列开始
#     for j in range(2, 41):
#         if getPrice(i,j) is not None:
#             p = sgm.SpotMarketChina(Commodity="散装国标一级豆油", Date=getDate(i), State=getStateByRegion("豆油", getRegion(j)),
#                                     Region=getRegion(j),
#                                     Price=getPrice(i,j))
#             sgm.session.add(p)
#             try:
#                 sgm.session.commit()
#             except:
#                 pass
#             sgm.session.close()
#
#     for j in range(42, 64):
#         if getPrice(i,j) is not None:
#             p = sgm.SpotMarketChina(Commodity="国标四级菜籽油", Date=getDate(i), State=getStateByRegion("菜油", getRegion(j)),
#                                     Region=getRegion(j),
#                                     Price=getPrice(i,j))
#             sgm.session.add(p)
#             try:
#                 sgm.session.commit()
#             except:
#                 pass
#             sgm.session.close()
#
#     for j in range(65, 72):
#         if getPrice(i,j) is not None:
#             p = sgm.SpotMarketChina(Commodity="24度棕榈油", Date=getDate(i), State=getStateByRegion("棕榈油", getRegion(j)),
#                                     Region=getRegion(j),
#                                     Price=getPrice(i,j))
#             sgm.session.add(p)
#             try:
#                 sgm.session.commit()
#             except:
#                 pass
#             sgm.session.close()