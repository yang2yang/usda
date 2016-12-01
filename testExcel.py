import xlrd
fileName = "ExportSalesDataByCommodity1.xls"

data = xlrd.open_workbook(fileName)

table = data.sheets()[0]

print(table.nrows,table.ncols)

# 从7开始
# ['', 'Soybeans', 42327.0, '', 'BANGLADESH', 952.0, 163866.0, 169224.0, 55000.0, 55000.0, 333090.0, 0.0, 0.0, 'Metric Tons']
for i in range(7,table.nrows):
    print(table.row_values(i))
    recode = table.row_values(i)
    print(xlrd.xldate.xldate_as_datetime(recode[2], 0))

    print(recode[1])

print(table.row_values(9999))

# for i in range(1000):
#     print(table.row_values(i))
# print(xlrd.xldate.xldate_as_datetime(table.cell(14,2).value,0))