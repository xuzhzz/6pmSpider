from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from lxml import etree
import re
# import random
# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["phantomjs.page.settings.userAgent"] = (random.choice(USER_AGENTS))
# dcap["phantomjs.page.settings.loadImages"] = False
# user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
# service_args = ['--ignore-ssl-errors=true', '--ssl-protocol=any']
#
# cap = webdriver.DesiredCapabilities.PHANTOMJS
# cap["phantomjs.page.settings.resourceTimeout"] = 1000
# cap["phantomjs.page.settings.loadImages"] = True
# cap["phantomjs.page.settings.disk-cache"] = True
# cap["phantomjs.page.settings.userAgent"] = user_agent,
# cap["phantomjs.page.customHeaders.User-Agent"] = user_agent,

def get_sku(page):
    html = etree.HTML(page)
    stock = html.xpath("string(//div[@class='_30wtU']/div[@class='_17Dby']/form/div[@class='_3Djr9']/div[@class='_1ynLL']/div[@class='_1rUc_'])")
    if stock:
        return re.search(r'(\d+)', stock).group(1)
    rest = html.xpath("string(//div[@class='_30wtU']/div[@class='_17Dby']/form//button)")
    print('rest:  ', rest)
    if rest == 'Out of Stock':
        return '0'
    return 'well-stocked'


def get_stock(url='https://www.6pm.com/p/lifestride-spark-red/product/8872328/color/585'):
    driver = webdriver.Chrome()
    # driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)
    # driver = webdriver.PhantomJS()
    # wait = WebDriverWait(driver, 10)
    # url = 'https://www.6pm.com/p/lifestride-spark-red/product/8872328/color/585'
    # url = 'https://www.6pm.com/p/bandolino-yara-natural-synthetic/product/8599315/color/59416'
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    try:
        driver.get(url)
    except TimeoutException:
        pass
    try:
        s_color = Select(driver.find_element_by_xpath(
            "//div[@class='_30wtU']/div[@class='_17Dby']/form/div[@class='VrH5P']/div[@class='Dcl_8']/select[@id='pdp-color-select']"))
    except NoSuchElementException:
        s_color = None

    try:
        s_size = Select(driver.find_element_by_xpath(
            "//div[@class='_30wtU']/div[@class='_17Dby']/form/div[@class='_1KSLq']/div[@class='VrH5P'][1]/div[@class='Dcl_8']/select[@id='pdp-size-select']"))
    except NoSuchElementException:
        s_size = None

    try:
        s_width = Select(driver.find_element_by_xpath(
            "//div[@class='_30wtU']/div[@class='_17Dby']/form/div[@class='_1KSLq']/div[@class='VrH5P'][2]/div[@class='Dcl_8']/select[@id='pdp-width-select']"))
    except NoSuchElementException:
        s_width = None

    s_color_list = []
    if s_color:
        for sc in s_color.options:
            if not sc.text.startswith('Select'):
                s_color_list.append(sc.text)
    else:
        s_color_list.append(driver.find_element_by_xpath(
            "//div[@class='_30wtU']/div[@class='_17Dby']/form/div[@class='VrH5P']/div[@class='_24jH2']").text)
    print(s_color_list)

    s_size_list = []
    if s_size:
        for ss in s_size.options:
            if not ss.text.startswith('Select'):
                s_size_list.append(ss.text)
    else:
        s_size_list.append(driver.find_element_by_xpath(
            "//div[@class='_30wtU']/div[@class='_17Dby']/form/div[@class='_1KSLq']/div[@class='VrH5P'][1]/div[@class='_24jH2']").text)
    print(s_size_list)

    s_width_list = []
    if s_width:
        for sw in s_width.options:
            if not sw.text.startswith('Select'):
                s_width_list.append(sw.text)
    else:
        s_width_list.append(driver.find_element_by_xpath(
            "//div[@class='_30wtU']/div[@class='_17Dby']/form/div[@class='_1KSLq']/div[@class='VrH5P'][2]/div[@class='_24jH2']").text)
    print(s_width_list)

    # print(driver.find_element_by_xpath("//div[@class='vUkNo']").text)
    res = []
    print(4)
    for sc in s_color_list:
        for sz in s_size_list:
            for sw in s_width_list:
                if s_color:
                    s_color.select_by_visible_text(sc)
                if s_size:
                    s_size.select_by_visible_text(sz)
                if s_width:
                    s_width.select_by_visible_text(sw)
                page = driver.page_source
                res.append([sc, sz, sw, get_sku(page)])

    driver.close()
    return res


if __name__ == '__main__':
    print(get_stock())
