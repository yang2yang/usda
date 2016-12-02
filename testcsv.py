import csv

import csv
from datetime import datetime
import time

startTime = time.time()

with open('CY2016.csv', newline='') as f:
    reader = csv.reader(f)
    # print(type(reader))
    for row in reader:
        # print(type(row[0]),row[1],row[2])
        print(row)

s = "20161110"
print(datetime.strptime(s, '%Y%m%d').date())

endTime = time.time()

print(endTime - startTime)
