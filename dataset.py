import pandas as pd

from typing import Tuple
from crawler import Crawler


class Dataset:
    """
    A class representing a dataset.

    Attributes:
        crawler (Crawler): An instance of the Crawler class.
        _dataset (pandas.DataFrame): The concatenated dataset.

    Methods:
        __init__(self, sleep: int = 10): Initializes the Dataset object.
        get_data(self): Retrieves data using the crawler.
        dataset(self): Returns the concatenated dataset.

    """

    def __init__(self, sleep: int = 10):
        self.crawler = Crawler(sleep)
        self.get_data()
        car_info = self._reset_index(pd.concat([*self.crawler.car_info]))
        faq = self._reset_index(self.crawler.faq)
        self._dataset = car_info, faq

    def _reset_index(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Reset the index of the given dataset.

        Parameters:
        - dataset (pd.DataFrame): The dataset to reset the index of.

        Returns:
        - pd.DataFrame: The dataset with the index reset.
        """
        dataset.index = range(len(dataset.index))

        return dataset

    def get_data(self):
        """
        Retrieves data using the crawler.

        This method iterates over a range of values and calls the `get` method of the crawler.

        """

        for i in range(1, 3):
            self.crawler.get_car_info(i)

        self.crawler.get_faq()

    @property
    def dataset(self) -> pd.DataFrame:
        """
        Returns the concatenated dataset.

        Returns:
            pandas.DataFrame: The concatenated dataset.

        """

        return self._dataset


def load_dataset(sleep: int = 10) -> Tuple[pd.DataFrame]:
    return Dataset(sleep).dataset
