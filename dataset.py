import pandas as pd

from typing import List
from crawler import Crawler


class Dataset:
    """
    A class representing a dataset.

    Attributes:
        crawler (Crawler): An instance of the Crawler class.
        _dataset (pandas.DataFrame): The concatenated dataset.

    Methods:
        __init__(): Initializes the Dataset object.
        get_data(): Retrieves data using the crawler.
        dataset(): Returns the concatenated dataset.

    """

    def __init__(self, sleep: int = 10):
        self.crawler = Crawler(sleep)
        self.get_data()
        car_info = pd.concat([*self.crawler.car_info])
        faq = self.crawler.faq
        car_info.index = range(len(car_info.index))
        faq.index = range(len(faq.index))
        self._dataset = car_info, faq

    def get_data(self):
        """
        Retrieves data using the crawler.

        This method iterates over a range of values and calls the `get` method of the crawler.

        """
        for i in range(1, 3):
            self.crawler.get_car_info(i)
        self.crawler.get_faq()

    @property
    def dataset(self):
        """
        Returns the concatenated dataset.

        Returns:
            pandas.DataFrame: The concatenated dataset.

        """
        return self._dataset


def load_dataset(sleep: int = 10) -> List[pd.DataFrame]:
    return Dataset(sleep).dataset
