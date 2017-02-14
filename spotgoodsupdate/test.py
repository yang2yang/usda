import time

from datetime import datetime
import spotusmodel
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import bs4
import os

pathName = r'C:\Users\admin\Downloads'

def delete():
    n = 0
    for root, dirs, files in os.walk(pathName):
        for name in files:
            if (name == 'report.xls'):
                n += 1
                print(n)
                os.remove(os.path.join(root, name))


# 检查是否有report.xls,如果有就删除   本质上xls是一个html文件

def getExcelSoyBeanMeal():
    driver = webdriver.Chrome()
    url = "https://marketnews.usda.gov/mnp/ls-report-config"
    driver.get(url)
    # 强行暂停5s
    driver.implicitly_wait(5)
    # 选择类别
    selectCategory = Select(driver.find_element_by_name("category"))
    selectCategory.select_by_value("Feedstuff")
    # 选择品种
    selectCommodity = Select(driver.find_element_by_name("subComm"))
    selectCommodity.select_by_value("SOYBEAN MEAL HIGH PROTEIN")
    # 选择
    selectPublication = Select(driver.find_element_by_name("repType"))
    selectPublication.select_by_value("Daily")
    # 选择地点
    selectLocation = Select(driver.find_element_by_name("loc"))
    selectLocation.select_by_value("All")
    # 选择品种详细情况
    selectCommDetail = Select(driver.find_element_by_name("commDetail"))
    selectCommDetail.select_by_value("All")
    # 选择开始的时间
    repDate = driver.find_element_by_name("repDate")
    repDate.send_keys("01/01/2017")
    # 选择结束的时间
    endDate = driver.find_element_by_name("endDate")
    today = time.strftime('%m/%d/%Y', time.localtime(time.time()))
    endDate.send_keys(today)
    # 点击run按钮
    run = driver.find_element_by_name("run")
    run.send_keys(Keys.RETURN)
    # 下载Excel文件
    excelLink = driver.find_element_by_partial_link_text("Excel")
    excelLink.send_keys(Keys.RETURN)


def getExcelSoyBeanOil():
    driver = webdriver.Chrome()
    url = "https://marketnews.usda.gov/mnp/ls-report-config"
    driver.get(url)
    # 强行暂停5s
    driver.implicitly_wait(5)
    # 选择类别
    selectCategory = Select(driver.find_element_by_name("category"))
    selectCategory.select_by_value("Feedstuff")
    # 选择品种
    selectCommodity = Select(driver.find_element_by_name("subComm"))
    selectCommodity.select_by_value("SOYBEAN OIL")
    # 选择
    selectPublication = Select(driver.find_element_by_name("repType"))
    selectPublication.select_by_value("Daily")
    # 选择地点
    selectLocation = Select(driver.find_element_by_name("loc"))
    selectLocation.select_by_value("All")
    # 美豆油不需要选择品种
    # selectCommDetail = Select(driver.find_element_by_name("commDetail"))
    # selectCommDetail.select_by_value("All")
    # 选择开始的时间
    repDate = driver.find_element_by_name("repDate")
    repDate.send_keys("01/01/2017")
    # 选择结束的时间
    endDate = driver.find_element_by_name("endDate")
    today = time.strftime('%m/%d/%Y', time.localtime(time.time()))
    endDate.send_keys(today)
    # 点击run按钮
    run = driver.find_element_by_name("run")
    run.send_keys(Keys.RETURN)
    # 下载Excel文件
    excelLink = driver.find_element_by_partial_link_text("Excel")
    excelLink.send_keys(Keys.RETURN)

def getExcelSoyBeans():
    driver = webdriver.Chrome()
    url = "https://marketnews.usda.gov/mnp/ls-report-config"
    driver.get(url)
    # 强行暂停5s
    driver.implicitly_wait(5)
    # 选择类别
    selectCategory = Select(driver.find_element_by_name("category"))
    selectCategory.select_by_value("Grain")
    # 有机？
    selectOrganic = Select(driver.find_element_by_name("organic"))
    selectOrganic.select_by_value("NO")
    # 选择品种
    selectCommodity = Select(driver.find_element_by_name("commodity"))
    selectCommodity.select_by_value("Oil Seed")
    # 选择子品种
    selectCommodity = Select(driver.find_element_by_name("subComm"))
    selectCommodity.select_by_value("Soybeans")
    # 选择
    selectPublication = Select(driver.find_element_by_name("repType"))
    selectPublication.select_by_value("Daily")
    # 选择地点
    selectLocation = Select(driver.find_element_by_name("loc"))
    selectLocation.select_by_value("All")
    # 选择品种详细情况
    selectCommDetail = Select(driver.find_element_by_name("commDetail"))
    selectCommDetail.select_by_value("All")
    # 选择开始的时间
    repDate = driver.find_element_by_name("repDateGrain")
    repDate.send_keys("01/01/2017")
    # 选择结束的时间
    endDate = driver.find_element_by_name("endDateGrain")
    today = time.strftime('%m/%d/%Y', time.localtime(time.time()))
    endDate.send_keys(today)
    # 点击run按钮
    run = driver.find_element_by_name("run")
    run.send_keys(Keys.RETURN)
    # 下载Excel文件
    excelLink = driver.find_element_by_partial_link_text("Excel")
    excelLink.send_keys(Keys.RETURN)

def parse():
    fileName = r"C:\Users\admin\Downloads\report.xls"
    fileName = pathName+"\\report.xls"

    soup = bs4.BeautifulSoup(open(fileName).read(), "html.parser")

    tablelist = []
    for table in soup.findAll('table'):
        for row in table.findAll('tr'):
            trlist = []
            for td in row.findAll('td'):
                trlist.append(td.text)
            tablelist.append(trlist)
    print(tablelist)
    return tablelist


def save(tablelist,commodity):
    for row in tablelist:
        if len(row) != 0:
            p = spotusmodel.SpotmarketUs(Commodity=commodity, Date=datetime.strptime(row[0], '%m/%d/%Y').date(),
                                         Location=row[1], Category=row[2],
                                         Variety=row[3], GradeDescription=row[4], Units=row[5], Transmode=row[6],
                                         BidLow=row[7], BidHigh=row[8], PricingPoint=row[9], DeliveryPeriod=row[10])
            spotusmodel.session.add(p)
            try:
                spotusmodel.session.commit()
            except:
                # 不能使用pass，必须要使用rollback??
                spotusmodel.session.rollback()

def run():
    delete()
    getExcelSoyBeanMeal()
    time.sleep(10)
    save(parse(),"soybeanmeal")

    delete()
    getExcelSoyBeanOil()
    time.sleep(10)
    save(parse(),"soybeanoil")


    delete()
    getExcelSoyBeans()
    time.sleep(10)
    save(parse(),"soybeans")


run()


