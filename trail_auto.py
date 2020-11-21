import telegram
from selenium import webdriver
import getpass
import time

def telegram_config():
    my_token = "1461046500:AAFHgxklEQch_ANMZnF8T_WWCivwrW3AQLo"
    bot = telegram.Bot(token=my_token)  # bot을 선언합니다.
    updates = bot.getUpdates()  # 업데이트 내역을 받아옵니다.

    for u in updates:  # 내역중 메세지를 출력합니다.
        print(u.message)

def selenium_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('windows-size=1920*1080')

    driver = webdriver.Chrome('chromedriver.exe')

    return driver

def get_id():

    #id = input('ID: ')
    id = "1765442377"

    return id

def get_password():

    pw = getpass.getpass('PW: ')

    return pw

def train_reservation(start, tr_length):
    while start < tr_length:
        try:
            while True:
                # 좌석매진(Alt 값), 예약하기(Alt 값)
                text = driver.find_element_by_xpath("//tbody/tr[{}]/td[6]//img".format(start)).get_attribute('alt')

                if text == "예약하기":
                    driver.find_element_by_xpath("//tbody/tr[{}]/td[6]//img".format(start)).click()
                    telegram_config()
                    break

                if start == tr_length - 1:
                    start = 1
                    driver.refresh()
        except:
            break

if __name__ == "__main__":

    i = 0

    id = get_id()
    password = get_password()

    start_point = input('출발지: ')
    end_point = input('도착지: ')
    start_date = input("출발일(ex. 20201111): ")

    url = 'http://www.letskorail.com/korail/com/login.do'

    driver = selenium_driver()

    driver.get(url)

    # 로그인
    driver.find_element_by_id('txtMember').send_keys(id)
    driver.find_element_by_id('txtPwd').send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginDisplay1"]/ul/li[3]/a/img').click()

    popup_count = len(driver.window_handles)
    i = popup_count

    # 팝업창 제거
    while i > 0:
        if i == 1:
            driver.switch_to.window(driver.window_handles[i-1])
            break
        else:
            driver.switch_to.window(driver.window_handles[i-1])
            driver.close()
            i -= 1

    driver.find_element_by_xpath('//*[@id="txtGoStart"]').clear()
    driver.find_element_by_xpath('//*[@id="txtGoStart"]').send_keys(start_point)

    driver.find_element_by_xpath('//*[@id="txtGoEnd"]').clear()
    driver.find_element_by_xpath('//*[@id="txtGoEnd"]').send_keys(end_point)

    driver.find_element_by_xpath('//*[@id="res_cont_tab01"]/form/div/fieldset/ul[2]/li[1]/a/img').click()

    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_id("d{}".format(start_date)).click()
    driver.switch_to.window(driver.window_handles[0])

    driver.implicitly_wait(1)
    driver.find_element_by_xpath('//*[@id="res_cont_tab01"]/form/div/fieldset/p/a/img').click()
    driver.implicitly_wait(3)

    tr_length = len(driver.find_elements_by_xpath("//tbody//tr"))
    train_reservation(1, tr_length)

