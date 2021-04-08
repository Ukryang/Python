from selenium import webdriver
import requests
import json
import time
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

## 예약 가능 날짜 출력 함수
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

    ## 예약 가능 날짜 확인을 POST로 JSON 데이터 전송
    header = {
        "Referer": "https://booking.hanwharesort.co.kr/pzc/pnr/0010/serviceM00.mvc?authKey=cd053845ca1f4cbab714a94020adeaeb",
    }

    # BRCH_CH: 0100(설악) 0400(용인) 1100(제주) 1800(골든베이)
    data = { "INTF_ID" : "TFO00HBSGOLREM9071",
    		 "RECV_SVC_CD" : "HBSGOLREM9071",
    		 "DATA_NAME_I" : "ds_search",
    		 "CORP_CD" : "1000",
    		 "BRCH_CD" : BRCH_CD,
             "CUST_NO": "0002545441",
    		 "CUST_CL_CD" : "",
    		 "INPUT_DIV_CD" : "20",
    		 "RSRV_START_MON" : "202104",
    		 "RSRV_END_MON" : "202105",
    		 "MEMB_NO" : "",
    		 "EMPLR_YN" : "N" }

    url = "https://booking.hanwharesort.co.kr/pzc/pnr/0010/doExecute.mvc"
    res = requests.post(url=url, headers=header, data=data)

    # 비교를 위한 현재 날짜 선언
    today = datetime.today().strftime("%Y%m%d")

    # 전송 상태 체크
    if res.status_code == requests.codes.ok:
        reservation_data = json.loads(res.text)
        for data in reservation_data['ds']['Data']['ds_cldrList']:

            # 쓰레기 값 제외(지난 날짜 및 예약 비 활성화)
            if data['REMNDR_CNT'] != 0 and data['RSRV_DATE'] > today and data['REMNDR_CNT'] < 20:
                print("날짜: {} / 예약 가능 팀: {}" .format(data['RSRV_DATE'], data['REMNDR_CNT']))

    RSRV_DATE = input("\n예약 날짜 입력: ")

    # 달력 이동을 위한 현재 월 확인
    RSRV_MONTH = RSRV_DATE[4:6]

    return BRCH_CD, li_number, RSRV_DATE, RSRV_MONTH

## 예약 가능 시간 출력 함수
# def reservation_time(BRCH_CD, li_number):
#
#     RSRV_DATE = input("예약 날짜 입력: ")
#
#     # 달력 이동을 위한 현재 월 확인
#     RSRV_MONTH = RSRV_DATE[4:6]
#
#     ## 예약 가능 시간 확인을 POST로 JSON 데이터 전송
#     header = {
#         "Referer": "https://booking.hanwharesort.co.kr/pzc/pnr/0010/serviceS01.mvc?targetDate={}&branchCode={}".format(BRCH_CD, RSRV_DATE),
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
#     }
#
#     # BRCH_CH: 0100(설악) 0400(용인) 1100(제주) 1800(골든베이)
#     # RSRV_DATE: YYYYMMDD
#     data = { "INTF_ID" : "TFO00HBSGOLREM9081",
#     		 "RECV_SVC_CD" : "HBSGOLREM9081",
#     		 "DATA_NAME_I" : "ds_search",
#     		 "CORP_CD" : "1000",
#     		 "BRCH_CD" : BRCH_CD,
#              "RSRV_DATE": RSRV_DATE,
#     		 "RNDG_DIV_CD": "%",
#              "INPUT_DIV_CD": "20",
#              "EMP_NO": "",
#              "HOLE_DIV_CD": "1",
#              "EMPLR_YN": "N",
#              "CONT_NO": ""  }
#
#     url = "https://booking.hanwharesort.co.kr/pzc/pnr/0010/doExecute.mvc"
#     res2 = requests.post(url=url, headers=header, data=data)
#
#     # 전송 상태 체크
#     # if res2.status_code == requests.codes.ok:
#     #     stock_data = json.loads(res2.text)
#     #     for data in stock_data['ds']['Data']['ds_list']:
#     #         print("예약 가능 시간: {} / 예약 가능 코스: {}".format(data['RSRV_TIME'], data['RSRV_CORS_NM']))
#     #
#     # # 예약 시간 입력
#     # RSRV_TIME = input("예약 시간 입력: ")
#     # RSRV_CORS_NM = input("예약 코스 입력: ")
#
#     return RSRV_DATE, RSRV_MONTH, RSRV_TIME, RSRV_CORS_NM

if __name__ == "__main__":

    i = 0

    id = login.id()
    password = login.password()

    now_month = time.strftime("%m", time.localtime())

    club = input("클럽 입력: ")
    BRCH_CD, li_number, RSRV_DATE, RSRV_MONTH = reservation_date(club)
    #RSRV_DATE, RSRV_MONTH, RSRV_TIME, RSRV_CORS_NM = reservation_time(BRCH_CD, li_number)

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

    temp = int(RSRV_MONTH) - int(now_month)
    count = 0

    if temp > 0:
        while count < temp:
            driver.find_element_by_xpath('//*[@id="nextMonthBtn"]').click()
            count += 1
        day = driver.find_element_by_xpath('//*[@id="date{}"]/strong'.format(RSRV_DATE)).click()
    else:
        day = driver.find_element_by_xpath('//*[@id="date{}"]/strong'.format(RSRV_DATE)).click()

    time.sleep(3)
    iframe = driver.find_element_by_id('iframeTeeTime2')
    driver.switch_to.frame(iframe)
    time.sleep(1)

    tr_length = len(driver.find_elements_by_xpath('//table[2]/tbody/tr'))
    tr_count = 2
    #/ html / body / form / div / div[2] / div[5] / table[2] / tbody / tr[17] / td[5] / a


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
                print("\nGoing to Reservation Page....")
                driver.find_element_by_xpath('//table[2]/tbody/tr[{}]/td[5]/a'.format(tr_count)).click()
                break
            tr_count += 1
        except:
            print("Error!! Please check the script")
            break

    time.sleep(3)
    driver.switch_to.frame("iframeTeeTime")
    #driver.find_element_by_xpath('//*[@id="btnConfirm"]').click()






