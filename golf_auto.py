from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pyautogui
import json
import time
from get_credentials import login
from datetime import datetime

def selenium_driver():

    options = webdriver.ChromeOptions()
    options.add_argument('windows-size=1920*1080')
    options.add_argument('disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome('chromedriver.exe')

    return driver

if __name__ == "__main__":

    i = 0

    id = login.id()
    password = login.password()

    club = input("클럽 입력: ")

    # 마우스 포지션
    # 용인: 75, 설악: 135, 골든베이: 210, 제주: 275
    club_mouse_position = [75, 135, 210, 275]

    if club == "용인":
        club_mouse_x = club_mouse_position[0]
    elif club == "설악":
        club_mouse_x = club_mouse_position[1]
    elif club == "골든베이":
        club_mouse_x = club_mouse_position[2]
    elif club == "제주":
        club_mouse_x = club_mouse_position[3]
    else:
        print("설악, 용인, 제주, 골든베이 중에 입력하세요!!")

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

    time.sleep(3)
    chks = driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div[2]/a[2]/img')
    for chk in chks:
        chk.click()

    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)
    secreenwidth, secreenheigth = pyautogui.size()
    print(secreenwidth, secreenheigth)

    pyautogui.click(x=club_mouse_x, y=340)
    scr = pyautogui.screenshot()
    # 달력 다음 칸 y+55
    mpos = pyautogui.position(x=75, y=645)
    mpos2 = pyautogui.position(x=75, y=810)
    mpos3 = pyautogui.position(x=93, y=579)

    print(scr.getpixel(mpos))
    print(scr.getpixel(mpos2))
    print(scr.getpixel(mpos3))




    # club = input("클럽 입력: ")
    #
    # if club == "설악":
    #     BRCH_CD = "0100"
    # elif club == "용인":
    #     BRCH_CD = "0400"
    # elif club == "제주":
    #     BRCH_CD = "1100"
    # elif club == "골든베이":
    #     BRCH_CD = "1800"
    # else:
    #     print("설악, 용인, 제주, 골든베이 중에 입력하세요!!")
    #
    # header = {
    #     "Referer": "https://booking.hanwharesort.co.kr/pzc/pnr/0010/serviceM00.mvc?authKey=404475cff6ec407bb7642f33f4b4676c",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    # }
    # # BRCH_CH: 0100(설악) 0400(용인) 1100(제주) 1800(골든베이)
    # data = { "INTF_ID" : "TFO00HBSGOLREM9071",
    # 		 "RECV_SVC_CD" : "HBSGOLREM9071",
    # 		 "DATA_NAME_I" : "ds_search",
    # 		 "CORP_CD" : "1000",
    # 		 "BRCH_CD" : BRCH_CD,
    # 		 "CUST_NO" : "0002545441",
    # 		 "CUST_CL_CD" : "",
    # 		 "INPUT_DIV_CD" : "20",
    # 		 "RSRV_START_MON" : "202011",
    # 		 "RSRV_END_MON" : "202012",
    # 		 "MEMB_NO" : "",
    # 		 "EMPLR_YN" : "N" }
    #
    # url = "https://booking.hanwharesort.co.kr/pzc/pnr/0010/doExecute.mvc"
    # res = requests.post(url=url, headers=header, data=data)
    #
    # today = datetime.today().strftime("%Y%m%d")
    #
    # if res.status_code == requests.codes.ok:
    #     stock_data = json.loads(res.text)
    #     for data in stock_data['ds']['Data']['ds_cldrList']:
    #         if data['REMNDR_CNT'] != 0 and data['RSRV_DATE'] > today :
    #             print("날짜: {} / 예약 가능 팀: {}" .format(data['RSRV_DATE'], data['REMNDR_CNT']))
    #
    # RSRV_DATE = input("예약 날짜 입력: ")
    # header = {
    #     "Referer": "https://booking.hanwharesort.co.kr/pzc/pnr/0010/serviceS01.mvc?targetDate={}&branchCode={}".format(BRCH_CD, RSRV_DATE),
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    # }
    # # BRCH_CH: 0100(설악) 0400(용인) 1100(제주) 1800(골든베이)
    # data = { "INTF_ID" : "TFO00HBSGOLREM9081",
    # 		 "RECV_SVC_CD" : "HBSGOLREM9081",
    # 		 "DATA_NAME_I" : "ds_search",
    # 		 "CORP_CD" : "1000",
    # 		 "BRCH_CD" : BRCH_CD,
    #          "RSRV_DATE": RSRV_DATE,
    # 		 "RNDG_DIV_CD": "%",
    #          "INPUT_DIV_CD": "20",
    #          "EMP_NO": "",
    #          "HOLE_DIV_CD": "1",
    #          "EMPLR_YN": "N",
    #          "CONT_NO": ""  }
    #
    # url = "https://booking.hanwharesort.co.kr/pzc/pnr/0010/doExecute.mvc"
    #
    # res2 = requests.post(url=url, headers=header, data=data)
    # if res2.status_code == requests.codes.ok:
    #
    #     stock_data = json.loads(res2.text)
    #     for data in stock_data['ds']['Data']['ds_list']:
    #        print(data)

##################################################################################################################################################

    # # doExecute.mvc #1 - 시간 예역
    # header = {
    #     "Referer": "https://booking.hanwharesort.co.kr/pzc/pnr/0010/serviceS01.mvc?targetDate={}&branchCode={}".format(BRCH_CD, RSRV_DATE),
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    # }
    #
    # data = {
    #     "INTF_ID": "TFO00HBSGOLREM9085",
    #     "RECV_SVC_CD": "HBSGOLREM9085",
    #     "DATA_NAME_I": "ds_search",
    #     "CORP_CD": "1000",
    #     "BRCH_CD": "1100",
    #     "RSRV_DATE": "20201224",
    #     "MEMB_NO": "",
    #     "CUST_NO": "0002545441"
    # }
    #
    # url = "https://booking.hanwharesort.co.kr/jpg/cmn/doExecute.mvc"
    # res = requests.post(url=url, headers=header, data=data, allow_redirects=False)
    #
    # #doExecute.mvc #2 - 시간 예역
    # header = {
    #     "Referer": "https://booking.hanwharesort.co.kr/pzc/pnr/0010/serviceS01.mvc?targetDate={}&branchCode={}".format(BRCH_CD, RSRV_DATE),
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    # }
    #
    #
    # data = {
    #     "ds": {
    #         "ds_holding": [
    #             {
    #             "CORP_CD": "1000",
    #             "BRCH_CD": "1100",
    #             "TEEOFF_NO": "202000879663",
    #             "RSRV_NO": "",
    #             "HOLD_DIV": "INS"
    #             }
    #         ],
    #      "serviceInfo": {"INTF_ID": "TFO00HBSGOLREM0754", "RECV_SVC_CD": "HBSGOLREM0754"}}
    # }
    #
    # url = "https://booking.hanwharesort.co.kr/pzc/cmn/doExecute.mvc"
    #
    # res = requests.post(url=url, headers=header, data=data, allow_redirects=False)
    #
    #doExecute.mvc #3 - 시간 예역
    # header = {
    #     "Referer": "https://booking.hanwharesort.co.kr/pzc/pnr/0010/serviceS01.mvc?targetDate={}&branchCode={}".format(BRCH_CD, RSRV_DATE),
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    # }
    #
    #
    # data = {
    #     "ds": {
    #         "ds_rsrvdcsninf": [
    #             {
    #             "CORP_CD": "1000",
    #             "BRCH_CD": "1100",
    #             "TEEOFF_NO": "202000879663",
    #             "RSRV_NO": "",
    #             "PROMTN_NO":"",
    #             "DCSN_PRSN":"4",
    #             "DSCNT_DIV_CD":"",
    #             "DSCNT_AMT":"",
    #             "SPECL_SET_DIV_CD":"",
    #             "SPECL_SET_USE_YN":"",
    #             "RCEPT_ID":"ukryang@gmail.com"
    #             }
    #         ],
    #      "serviceInfo":{"INTF_ID":"TFO00HBSGOLREM0716","RECV_SVC_CD":"HBSGOLREM0716"}}
    # }
    #
    # url = "https://booking.hanwharesort.co.kr/pzc/cmn/doExecute.mvc"
    #
    # res = requests.post(url=url, headers=header, data=data, allow_redirects=False)

    # header = {
    #     "Referer": "https://booking.hanwharesort.co.kr/pzc/pnr/0010/serviceM00.mvc",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    # }
    # # BRCH_CH: 0100(설악) 0400(용인) 1100(제주) 1800(골든베이)
    # data = { "sRsrvDate": "20201224",
    #          "sTeeOffNo": "202000879663",
    #          "sTeeOffNo18": "",
    #          "sRsrvTime": "0853",
    #          "sBrchCd": "1100",
    #          "sRsrvCorsNm": "OUT코스",
    #          "sJontYn": "undefined",
    #          "sAddHole": "1",
    #          "sNrmltAmt": "",
    #          "sOnlineMembAmt": "",
    #          "sDscnRate": "",
    #          "sPromtnNo": "",
    #          "sRsrvNo": "2004450853" }
    #
    # url = "https://booking.hanwharesort.co.kr/pzc/pnr/0010/serviceS02.mvc"
    #
    # res = requests.post(url=url, headers=header, data=data)
    # html = res.text
    # soup = (html, "html.parser")
    # print(soup)


########################################################################################################################
#실제 예약 페이지

    # header = {
    #     "Referer": "https://booking.hanwharesort.co.kr/pzc/pnr/0010/serviceS02.mvc",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    # }
    # data = {
    #     "ds": {
    #         "ds_input": [
    #             {
    #                 "CORP_CD": "1000",
    #                 "BRCH_CD": "1100",
    #                 "TEEOFF_NO": "202000879663",
    #                 "RSRV_NO": "2004450871",
    #                 "RSRV_RECOG_NO": "",
    #                 "GOLF_RSRV_STAT_CD": "",
    #                 "RSRV_ATRB_CD": "",
    #                 "CHNNL_LCLAS_CD": "",
    #                 "CHNNL_MLSFC_CD": "",
    #                 "CHNNL_SCLAS_CD": "",
    #                 "RSRV_CUST_NM": "위욱량(9H)",
    #                 "CUST_NO": "0002545441",
    #                 "CUST_CL_CD": "222",
    #                 "MEMB_NO": "",
    #                 "CNTCTR_NM": "",
    #                 "TEL_NO1": "82",
    #                 "TEL_NO2": "010",
    #                 "TEL_NO3": "2527",
    #                 "TEL_NO4": "3402",
    #                 "RNDG_PRSN_CNT": "",
    #                 "NOCADD_YN": "",
    #                 "CADD_CNT": "",
    #                 "COMT": "9H 3인 ",
    #                 "ZKIDNO_MNO": "",
    #                 "PASSWORD": "",
    #                 "PERS_INFO_AGREE_YN": "",
    #                 "INPUT_DIV_CD": "20",
    #                 "INPUT_RSRV_GUBUN": "H",
    #                 "CYBER_ID": "ukryang@gmail.com",
    #                 "TGT_CORP_CD": "",
    #                 "JONT_YN": "",
    #                 "HOLE_DIV_CD": "",
    #                 "ACMPNY_PRSN_CNT": "",
    #                 "PROMTN_NO": "",
    #                 "CONT_NO": "",
    #                 "EMPLR_YN": "N"}
    #         ],
    #      "serviceInfo": {"INTF_ID": "TFO00HBSGOLREM9101", "RECV_SVC_CD": "HBSGOLREM9101"}
    #     }
    # }
    #
    # url = "https://booking.hanwharesort.co.kr/pzc/pnr/0010/doExecute.mvc"
    # res = requests.post(url=url, headers=header, data=data)
    # print(res.text)




