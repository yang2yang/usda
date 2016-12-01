import requests


r = requests.get("https://apps.fas.usda.gov/esrquery/esrq.aspx")
print(r.content)


r = requests.get("https://www.baidu.com")
print(r.content)