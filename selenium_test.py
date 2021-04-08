from selenium import webdriver
import getpass
import time

def selenium_driver():

    options = webdriver.ChromeOptions()
    # Headless 모드로 동작
    # options.add_argument('headless')
    # 크롬창 크기 지정
    # options.add_argument('window-size=1920x1080')
    # gpu 사용 하지 않음
    # options.add_argument('disable-gpu')
    # 개발 로그 숨기기
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome('chromedriver.exe', options=options)

    return driver

if __name__ == "__main__":

    id = input("ID: ")
    password = "dnldnrfid1!"

    url = 'https://www.plazacc.co.kr/plzcc/irsweb/golf2/member/login.do'
    driver = selenium_driver()
    driver.get(url)

    # 로그인
    driver.find_element_by_id('username').send_keys(id)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_xpath('//*[@id="btnLogin"]').click()

    # 현재 열려 있는 세션 확인
    print(driver.window_handles)

    # 열려 있는 세션 개수 확인
    popup_count = len(driver.window_handles)
    i = popup_count

    # 팝업창 제거
    while i > 0:
        if i == 1:
            driver.switch_to.window(driver.window_handles[i-1]) # 배열이 0부터 시작하므로 1을 빼줍니다.
            i = 0
            break
        else:
            driver.switch_to.window(driver.window_handles[i-1])
            driver.close()
            i -= 1

    # 잔여타임 예약 이동
    time.sleep(1)
    chks = driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div[2]/a[2]/img')
    for chk in chks:
        chk.click()

    # 클럽 선택
    # driver.find_element_by_xpath('//li[1]').click() #용인

    driver.switch_to.window(driver.window_handles[1])
    driver.switch_to.frame("iframeTeeTime")
    time.sleep(1)

    driver.find_element_by_xpath('//li[1]').click()
    time.sleep(1)