import os
import pandas as pd
from util.crawling import Crawling
from selenium.webdriver.common.by import By


if __name__ == "__main__":
    page = 1
    num = 1

    crawling = Crawling()
    path = f"https://car.encar.com/list/car?page={page}&search=%7B%22type%22%3A%22ev%22%2C%22action%22%3A%22(And.Hidden.N._.CarType.A._.GreenType.Y._.(Or.OfficeCityState.%EC%84%9C%EC%9A%B8._.OfficeCityState.%EA%B2%BD%EA%B8%B0._.OfficeCityState.%EC%9D%B8%EC%B2%9C._.OfficeCityState.%EB%8C%80%EC%A0%84._.OfficeCityState.%EC%84%B8%EC%A2%85._.OfficeCityState.%EC%B6%A9%EB%82%A8._.OfficeCityState.%EC%B6%A9%EB%B6%81._.OfficeCityState.%EA%B0%95%EC%9B%90._.OfficeCityState.%EB%B6%80%EC%82%B0._.OfficeCityState.%EB%8C%80%EA%B5%AC._.OfficeCityState.%EC%9A%B8%EC%82%B0._.OfficeCityState.%EA%B2%BD%EB%82%A8._.OfficeCityState.%EA%B2%BD%EB%B6%81._.OfficeCityState.%EA%B4%91%EC%A3%BC._.OfficeCityState.%EC%A0%84%EB%82%A8._.OfficeCityState.%EC%A0%84%EB%B6%81._.OfficeCityState.%EC%A0%9C%EC%A3%BC.)_.Separation.A.)%22%2C%22title%22%3A%22%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22MobileModifiedDate%22%7D"
    crawling.getBrowser(path, new_window=False)

    # 모달 닫기 버튼 누르기
    crawling.click_button('//*[@id="modal"]/div[2]/div/div/button[2]')

    # [‘차 이름’, ‘연식’, ‘키로수’, ‘가격’, ‘상세링크’]
    name_list = []
    year_list = []
    kilometer_list = []
    price_list = []
    link_list = []

    while True:
        if num != 218:
            print(num)
            if page == 1:
                path = f'//*[@id="__next"]/div[1]/div[3]/div[3]/div[{num}]'
                path2 = f'//*[@id="__next"]/div[1]/div[3]/div[3]/div[{num + 1}]'

                if (
                    crawling.find_ele_text(path) == ""
                    and crawling.find_ele_text(path2) == ""
                ):
                    page += 1
                    num = 1
                    continue
                elif (
                    crawling.find_ele_text(path) == ""
                    and crawling.find_ele_text(path2) != ""
                ):
                    num += 1
                    continue
                else:
                    try:
                        name = crawling.find_ele_text(path).split("\n")[1]
                        year = crawling.find_ele_text(path).split("\n")[2]
                        kilometer = crawling.find_ele_text(path).split("\n")[3]
                        price = crawling.find_ele_text(path).split("\n")[6]
                    except:
                        num += 1
                        continue

            elif page == 2:
                path = f'//*[@id="__next"]/div[1]/div[3]/div/div[{num}]'
                path2 = f'//*[@id="__next"]/div[1]/div[3]/div/div[{num + 1}]'

                if (
                    crawling.find_ele_text(path) == ""
                    and crawling.find_ele_text(path2) == ""
                ):
                    page += 1
                    num += 1
                    continue
                elif (
                    crawling.find_ele_text(path) == ""
                    and crawling.find_ele_text(path2) != ""
                ):
                    num += 1
                    continue
                else:
                    try:
                        name = crawling.find_ele_text(path).split("\n")[1]
                        year = crawling.find_ele_text(path).split("\n")[2]
                        kilometer = crawling.find_ele_text(path).split("\n")[3]
                        price = crawling.find_ele_text(path).split("\n")[6]
                    except:
                        num += 1
                        continue
            else:
                break

            num += 1
            name_list.append(name)
            year_list.append(year)
            kilometer_list.append(kilometer)
            price_list.append(price)

        elif num == 218:
            print("222222")
            num = 1
            page += 1

    crawling.close_connect()
    df = pd.DataFrame(
        {
            "차 이름": name_list,
            "연식": year_list,
            "키로수": kilometer_list,
            "가격": price_list,
        }
    )
    # result 파일 경로 만들기
    result_path = os.path.join(os.getcwd(), "data")
    os.makedirs(result_path, exist_ok=True)
    # csv로 저장
    df.to_csv(os.path.join(result_path, "result.csv"), index=False, encoding="utf-8")
    print(f'#### "result.csv"가 {result_path}에 저장되었습니다. ####')
