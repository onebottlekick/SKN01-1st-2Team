from typing import List

from dataset import load_dataset
from db import MySQLExecutor


def data_to_db(
    database: str, table_name: List[str], if_exists: str = "replace"
) -> None:
    mysql = MySQLExecutor(database)
    dataset, faq = load_dataset()
    mysql.df2sql(dataset, table_name, if_exists)
    mysql.df2sql(faq, "faq")


if __name__ == "__main__":
    data_to_db(database="encar", table_name="info")
