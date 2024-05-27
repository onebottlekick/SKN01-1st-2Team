# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


class Crawling:
    def __init__(self):
        self.new_window = False
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(options=self.options)
        self.browser.maximize_window()
        self.scroll_pos = 0

    def getBrowser(self, url="https://naver.com", new_window=True, option=None):
        self.browser.get(url)

    def find_ele_text(self, user_xpath):
        text = self.browser.find_element(By.XPATH, user_xpath).text.strip()
        return text

    def search_keword(self, user_xpath, item_name):
        self.browser.find_element(By.XPATH, user_xpath).send_keys(item_name)

    def click_button(self, button_xpath=None):
        try:
            self.browser.find_element(By.XPATH, button_xpath).click()
            print("버튼 클릭 성공")
        except Exception as e:
            print("By.XPATH로 클릭되지 않습니다. By.PARTIAL_LINK_TEXT로 접근합니다! ")
            time.sleep(2)
            try:
                totext = self.find_ele_text(button_xpath)  # 버튼 이름 텍스트로 가져와서
                self.browser.find_element(
                    By.PARTIAL_LINK_TEXT, totext
                ).click()  # By.PARTIAL_LINK_TEXT 안에 넣어줌

                print("성공!")
                if totext == None:  # 텍스트 받아오기를 실패하면 직접 이름 입력
                    print(
                        "해당 버튼의 키워드(이름)를 추가로 입력하세요. --> click_button(XPATH, 버튼 이름)"
                    )

            except Exception as e:
                print("문제발생!", type(e))

    # 스크롤 내려주는 함수
    # 픽셀값이 0이면 최상단. pixel 파라미터값만큼 이동 (defualt는 500씩 이동하도록 설정)
    def scroll_down(self, pixel=500, init_pos=False):
        try:
            if (
                init_pos == True
            ):  # 새로운 탭으로 전환할 경우 스크롤 위치 픽셀값을 최상단으로 초기화하기 위해 지정
                self.scroll_pos = 0

            self.browser.execute_script(
                f"window.scrollTo({self.scroll_pos}, {self.scroll_pos+pixel})"
            )  # (2) 해당위치에서 pixel만큼 이동하도록
            self.scroll_pos = (
                self.scroll_pos + pixel
            )  # (1) 스크롤값이 계속 저장되어서 ----------------------↑
            print("스크롤 다운 성공")

        except Exception as e:
            print("스크롤 다운 실패")
            print(e)

    def close_connect(self):
        self.browser.close()
        print("finished.")
        print(" ")

    def change_window(self):
        self.browser.switch_to.window(self.browser.window_handles[-1])
