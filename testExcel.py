from datetime import datetime

import xlrd
fileName = "ExportSalesDataByCommodity1.xls"
fileName = "CY2016.csv"
fileName = "USDA-SB.xlsx"
fileName = "wasde-12-10-2010.xls"

data = xlrd.open_workbook(fileName)

table = data.sheets()[0]
table = data.sheets()[8]

for i in range(table.nrows):
    recode = table.row_values(i)
    print(i,recode)
# print(table.ncols,table.nrows)

# 从7开始
# ['', 'Soybeans', 42327.0, '', 'BANGLADESH', 952.0, 163866.0, 169224.0, 55000.0, 55000.0, 333090.0, 0.0, 0.0, 'Metric Tons']
# for i in range(7,table.nrows):
#     print(table.row_values(i))
#     recode = table.row_values(i)
#     print(xlrd.xldate.xldate_as_datetime(recode[2], 0))
#
#     print(recode[1])

# print(table.row_values(9999))

# for i in range(1000):
#     print(table.row_values(i))
# print(xlrd.xldate.xldate_as_datetime(table.cell(14,2).value,0))

# for i in range(2,table.nrows):
#     print("table_nrows=",table.nrows)
#     print("i=",i)
#     recode = table.row_values(i)
#
#     for j in range(len(recode)):
#         if recode[j] == '':
#             recode[j] = None
#
#     if recode[2] is not None:
#         print(xlrd.xldate.xldate_as_datetime(recode[2], 0))
#
#     print(recode)
#     # print(xlrd.xldate.xldate_as_datetime(recode[2], 0))
#     # print(table.row_values(i))
#
#
print("aaa",table.cell(1,3).value)

print(datetime.strptime(table.cell(1,3).value,'%B %Y').date())