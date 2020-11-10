import selenium
from selenium import webdriver
import getpass
import time

def selenium_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('windows-size=1920*1080')

    driver = webdriver.Chrome('D:\Python\chromedriver.exe')

    return driver

def get_id():

    #id = input('ID: ')
    id = "1765442377"

    return id

def get_password():

    #pw = getpass.getpass('PW: ')
    pw = "solitude753!"

    return pw

if __name__ == "__main__":

    id = get_id()
    password = get_password()

    start_point = input('출발지: ')
    end_point = input('도착지: ')
    start_date = input("출발일(ex. 20201111): ")

    url = 'http://www.letskorail.com/korail/com/login.do'

    driver = selenium_driver()

    #day = input("날짜 입력: ")
    #time = input("시간 입력: ")

    driver.get(url)

    # 로그인
    driver.find_element_by_id('txtMember').send_keys(id)
    driver.find_element_by_id('txtPwd').send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginDisplay1"]/ul/li[3]/a/img').click()

    print(driver.window_handles)
    # 팝업창 제거
    driver.switch_to.window(driver.window_handles[2])
    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    driver.find_element_by_xpath('//*[@id="txtGoStart"]').clear()
    driver.find_element_by_xpath('//*[@id="txtGoStart"]').send_keys(start_point)

    driver.find_element_by_xpath('//*[@id="txtGoEnd"]').clear()
    driver.find_element_by_xpath('//*[@id="txtGoEnd"]').send_keys(end_point)

    driver.find_element_by_xpath('//*[@id="res_cont_tab01"]/form/div/fieldset/ul[2]/li[1]/a/img').click()
    print(driver.window_handles)

    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_id("d{}".format(start_date)).click()
    driver.switch_to.window(driver.window_handles[0])

    driver.implicitly_wait(1)
    driver.find_element_by_xpath('//*[@id="res_cont_tab01"]/form/div/fieldset/p/a/img').click()

    driver.find_element_by_name('btnRsv1_1').click()
    driver.implicitly_wait(1)
    driver.find_element_by_xpath('//*[@id="btn_next"]').click()

    # while count < 10:
    #     try:
    #         driver.find_element_by_name('btnRsv1_1').click()
    #         driver.find_elements_by_tag_name()
    #         driver.implicitly_wait(1)
    #         driver.find_element_by_xpath('//*[@id="btn_next"]').click()
    #
    #     count = count + 1
