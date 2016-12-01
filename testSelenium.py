from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

pattern = re.compile(r".*")

path = r'C:\Program Files (x86)\Mozilla Firefox'


# binary = FirefoxBinary(path)
# browser = webdriver.Firefox(firefox_binary=binary)

driver =  webdriver.Chrome()
url = "https://apps.fas.usda.gov/esrquery/esrq.aspx"
# driver.get("https://www.baidu.com")
driver.get(url)
assert "Export" in driver.title
print(driver.title)

elem = driver.find_element_by_id("ctl00_MainContent_btnSubmit")
elem.send_keys(Keys.RETURN)
# driver.implicitly_wait(60)
elems = driver.find_elements_by_class_name(pattern)
driver.find_elements()

print(elems)