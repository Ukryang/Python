from selenium import webdriver
import requests
import json
import time, re, argparse
from get_credentials import login
from datetime import datetime

def selenium_driver():

    options = webdriver.ChromeOptions()
    # Headless 모드로 동작
    # options.add_argument('headless')
    # 크롬창 크기 지정
    # options.add_argument('window-size=1920*1080')
    # gpu 사용 하지 않음
    # options.add_argument('disable-gpu')
    # 개발 로그 숨기기
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome('chromedriver.exe', options=options)

    return driver

def reservation_date(club):

    li_numbers = [1, 2, 3, 4]

    if club == "용인":
        li_number = li_numbers[0]
        BRCH_CD = "0400"
    elif club == "설악":
        li_number = li_numbers[1]
        BRCH_CD = "0100"
    elif club == "골든베이":
        li_number = li_numbers[2]
        BRCH_CD = "1800"
    elif club == "제주":
        li_number = li_numbers[3]
        BRCH_CD = "1100"
    else:
        print("설악, 용인, 제주, 골든베이 중에 입력하세요!!")

    return BRCH_CD, li_number

if __name__ == "__main__":

    now_month = time.strftime("%m", time.localtime())

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--month', required=True, type=int, default=now_month, help='Insert Month ex)03, 12')
    args = parser.parse_args()

    i = 0

    id = login.id()
    password = login.password()

    club = input("클럽 입력: ")
    BRCH_CD, li_number = reservation_date(club)

    url = 'https://www.plazacc.co.kr/plzcc/irsweb/golf2/member/login.do'
    driver = selenium_driver()
    driver.get(url)

    # 로그인
    driver.find_element_by_id('username').send_keys(id)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_xpath('//*[@id="btnLogin"]').click()

    popup_count = len(driver.window_handles)
    i = popup_count

    # 팝업창 제거
    while i > 0:
        if i == 1:
            driver.switch_to.window(driver.window_handles[i-1])
            i = 0
            break
        else:
            driver.switch_to.window(driver.window_handles[i-1])
            driver.close()
            i -= 1

    time.sleep(1)
    chks = driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div[2]/a[2]/img')
    for chk in chks:
        chk.click()

    driver.switch_to.window(driver.window_handles[1])
    driver.switch_to.frame("iframeTeeTime")
    time.sleep(1)

    driver.find_element_by_xpath('//li[{}]'.format(li_number)).click()
    time.sleep(1)

    temp = driver.find_element_by_xpath('//*[@id="calenderMonthTtl"]').get_attribute('innerHTML')
    site_month = re.split('. ', temp)
    site_month[1] = site_month[1].replace("0", "")

    temp = int(args.month) - int(site_month[1])
    count = 0

    if temp > 0:
        while count < temp:
            try:
                driver.find_element_by_xpath('//*[@id="nextMonthBtn"]').click()
                count += 1
            except:
                count += 1

    print("\n [{} 월]\n".format(args.month))
    teams = driver.find_elements_by_xpath('//table/tbody//a')

    try:
        for team in teams:
            date_temp = team.find_element_by_xpath('i').get_attribute('innerHTML')
            team_temp = team.find_element_by_xpath('strong').get_attribute('innerHTML')
            print("날짜: {}, 예약 가능한 팀: {}".format(date_temp, team_temp))
    except:
        print("예약 가능한 날짜가 없습니다...\n")

    RSRV_DATE = input("\n예약 날짜 입력: ")

    try:
        for team in teams:
            if RSRV_DATE == team.find_element_by_xpath('i').get_attribute('innerHTML'):
                team.find_element_by_xpath('i').click()
    except:
        print("예약 가능한 날짜가 없습니다...\n")

    time.sleep(3)
    iframe = driver.find_element_by_id('iframeTeeTime2')
    driver.switch_to.frame(iframe)
    time.sleep(1)

    tr_length = len(driver.find_elements_by_xpath('//table[2]/tbody/tr'))
    tr_count = 2

    while tr_count < tr_length + 1:
        try:
            srsvtime = driver.find_element_by_xpath('//table[2]/tbody/tr[{}]/td[5]/a'.format(tr_count)).get_attribute('srsrvtime')
            srscourse = driver.find_element_by_xpath('//table[2]/tbody/tr[{}]/td[5]/a'.format(tr_count)).get_attribute('srsrvcorsnm')
            print("예약 가능 시간: {} / 예약 가능 코스: {}".format(srsvtime, srscourse))
            tr_count += 1
        except:
            print("Error!! Please check the script")
            break

    tr_count = 2
    RSRV_TIME = input("\n예약 시간 입력: ")
    RSRV_CORS_NM = input("예약 코스 입력: ")

    while tr_count < tr_length + 1:
        try:
            srsvtime = driver.find_element_by_xpath('//table[2]/tbody/tr[{}]/td[5]/a'.format(tr_count)).get_attribute('srsrvtime')
            srscourse = driver.find_element_by_xpath('//table[2]/tbody/tr[{}]/td[5]/a'.format(tr_count)).get_attribute('srsrvcorsnm')

            if RSRV_TIME == srsvtime and RSRV_CORS_NM == srscourse:
                print("\nGoing to Reservation Page....\n")
                driver.find_element_by_xpath('//table[2]/tbody/tr[{}]/td[5]/a'.format(tr_count)).click()
                break
            tr_count += 1
        except:
            print("Error!! Please check the script")
            break

    time.sleep(3)
    driver.switch_to.frame("iframeTeeTime")
    #driver.find_element_by_xpath('//*[@id="btnConfirm"]').click()
