from dataset import load_dataset
from db import MySQLExecutor
from typing import List


def data_to_db(
    database: str, table_name: List[str], if_exists: str = "replace"
) -> None:
    mysql = MySQLExecutor(database)
    car_info, faq = load_dataset(2)
    mysql.df2sql(car_info, table_name[0], if_exists)
    mysql.df2sql(faq, table_name[1], if_exists)


if __name__ == "__main__":
    data_to_db(database="encar", table_name=["car_info", "faq"])
