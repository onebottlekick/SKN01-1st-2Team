import datetime
import time
from typing import Any, List
from urllib.parse import quote_plus

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


class Crawler:
    """
    A class that represents a web crawler for car data.
    """

    def __init__(self, sleep: int = 0):
        """
        Initializes the Crawler class.
        """

        self.sleep = sleep

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--incognito")
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )
        self.driver = webdriver.Chrome()

        self._car_info = []
        self._faq = None
        self.scroll_pos = 0

    def _get_url(self, page=None) -> str:
        """
        Generates the URL for car data based on the specified page number.

        Args:
            page (int): The page number. Defaults to None.

        Returns:
            str: The generated URL.
        """

        electrical = quote_plus("전기차")
        hybrid = quote_plus("하이브리드")
        p_hybrid = quote_plus("플러그인 하이브리드")
        lpg = quote_plus("LPG")
        page = page
        url = f"https://car.encar.com/list/car?page={page}&search=%7B%22type%22%3A%22ev%22%2C%22action%22%3A%22(And.Hidden.N._.CarType.A._.(C.GreenType.Y._.(Or.EvType.{electrical}._.EvType.{hybrid}._.EvType.{p_hybrid}._.EvType.{lpg}.))_.Separation.A.)%22%2C%22title%22%3A%22%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22MobileModifiedDate%22%7D"

        return url

    def _get_source(self, page: int):
        """
        Retrieves the HTML source code of the web page.

        Args:
            page (int): The page number to retrieve the source code from.

        Returns:
            str: The HTML source code of the web page.
        """

        self.driver.maximize_window()
        self.driver.get(self._get_url(page))
        self.driver.implicitly_wait(self.sleep)
        try:
            self.driver.implicitly_wait(5)
            close_banner = self.driver.find_element(
                By.XPATH, '//*[@id="modal"]/div[2]/div/div/button[2]'
            )
            close_banner.click()
        except:
            pass
        source = self.driver.page_source
        self.driver.implicitly_wait(1)
        return source

    def _process(self, soup: BeautifulSoup, tag: str, name_tag: str) -> List[Any]:
        """
        Processes the car data from the HTML soup.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object representing the HTML soup.
            tag (str): The class name of the car data container.
            name_tag (str): The class name of the car name element.

        Returns:
            List: The processed car data as a List.
        """

        def process_year(year):
            """
            Convert a string representing a year in the format 'yy/mm' to a datetime object.

            Args:
                year (str): A string representing a year in the format 'yy/mm'.

            Returns:
                datetime.datetime: A datetime object representing the converted year.

            """

            year = datetime.datetime.strptime(year, "%y/%m")

            return year

        car_list = soup.find_all("div", {"class", f"{tag}"})

        dataset = []
        for i in range(len(car_list)):
            name = (
                car_list[i]
                .find("strong", {"class": f"{name_tag}"})
                .text.strip()
                .replace("\n", " ")
            )
            info = [x.text.strip() for x in car_list[i].find_all("li")]
            year, km, f_type, city = info[:4]

            year = process_year(year.strip("식"))
            print("year", year)
            km = int(km.strip("km").replace(",", ""))

            data = [name, year, km, f_type, city]
            print(data)
            dataset.append(data)

        return dataset

    def process(self, soup) -> pd.DataFrame:
        """
        Processes the car data from the HTML soup.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object representing the HTML soup.

        Returns:
            pd.DataFrame: The processed car data as a DataFrame.
        """

        try:
            big = self._process(
                soup, "ItemBigImage_car__ovlrq", "ItemBigImage_name__h0biK"
            )
            small = self._process(
                soup, "ItemSmallImage_txt_area__79qyK", "ItemSmallImage_name__6Fim0"
            )
            big = pd.DataFrame(
                big, columns=["이름", "연식", "주행거리", "종류", "지역"]
            )
            small = pd.DataFrame(
                small, columns=["이름", "연식", "주행거리", "종류", "지역"]
            )
            dataset = pd.concat([big, small], axis=0)
            dataset = dataset.index = range(len(dataset.index))

        except:
            small = self._process(
                soup, "ItemSmallImage_txt_area__79qyK", "ItemSmallImage_name__6Fim0"
            )
            small = pd.DataFrame(
                small, columns=["이름", "연식", "주행거리", "종류", "지역"]
            )
            dataset = small

        return dataset

    def get_faq(self) -> pd.DataFrame:
        """
        Retrieves frequently asked questions (FAQ) from a website and stores them in a DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the questions and answers from the FAQ.
        """

        self.driver.get("http://www.encar.com/")
        time.sleep(2)
        self.driver.find_element(
            By.XPATH, "/html/body/div[1]/div[1]/ul[2]/li[3]/a"
        ).click()
        self.driver.find_element(
            By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div[4]/ul/li[2]/a"
        ).click()
        time.sleep(2)

        q_lst = []
        a_lst = []

        for i in range(5):
            try:
                self.driver.find_element(
                    By.XPATH,
                    f"/html/body/div[1]/div[2]/div[1]/div/form/div[3]/span[2]/a[{i+1}]",
                ).click()
                time.sleep(1)
                try:
                    for j in range(40):
                        if j % 2 == 0:
                            time.sleep(1)
                            q_xpath = f"/html/body/div[1]/div[2]/div[1]/div/form/span/div/ul/li[{j+1}]"
                            q = self.driver.find_element(By.XPATH, q_xpath).text.strip()
                            q_lst.append(q)
                        else:
                            self.driver.find_element(
                                By.XPATH,
                                f"/html/body/div[1]/div[2]/div[1]/div/form/span/div/ul/li[{j}]/a",
                            ).click()
                            time.sleep(1)
                            a_xpath = f'/html/body/div[1]/div[2]/div[1]/div/form/span/div/ul/li[{j+1}]/div[@class="text"]'
                            a = self.driver.find_element(By.XPATH, a_xpath).text.strip()
                            a_lst.append(a)
                except Exception as e:
                    print(f"{e}")
                    continue

            except Exception as e:
                print(f"{e}")
                continue

        max_len = max(len(q_lst), len(a_lst))
        q_lst += [""] * (max_len - len(q_lst))
        a_lst += [""] * (max_len - len(a_lst))

        df = pd.DataFrame({"질문": q_lst, "답변": a_lst})

        self._faq = df

    def get_car_info(self, page: int = 1):
        """
        Retrieves the car data from the web page.

        Args:
            page (int): The page number. Defaults to 1.
        """

        source = self._get_source(page)
        soup = BeautifulSoup(source, "html.parser")
        dataset = self.process(soup)
        self._car_info.append(dataset)

    @property
    def car_info(self):
        """
        Returns the dataset containing the car data.

        Returns:
            dict: The dataset containing the car data.
        """

        return self._car_info

    @property
    def faq(self):
        """Returns the FAQ (Frequently Asked Questions) of the crawler."""

        return self._faq
