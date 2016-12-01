import requests


r = requests.get("https://apps.fas.usda.gov/esrquery/esrq.aspx")
print(r.content)


r = requests.get("https://www.baidu.com")
print(r.content)

for i in range(100):
    print(i)