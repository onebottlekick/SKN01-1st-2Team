from typing import List

from dataset import load_dataset
from db import MySQLExecutor


def data_to_db(
    database: str, table_name: List[str], if_exists: str = "replace"
) -> None:
    """
    Load dataset and FAQ data into the specified database.

    Args:
        database (str): The name of the database to load the data into.
        table_name (List[str]): A list of table names where the dataset and FAQ data will be stored.
        if_exists (str, optional): Specifies the behavior when the table already exists. Defaults to "replace".

    Returns:
        None
    """

    mysql = MySQLExecutor(database)
    dataset, faq = load_dataset()
    mysql.df2sql(dataset, table_name[0], if_exists)
    mysql.df2sql(faq, table_name[1], if_exists)


if __name__ == "__main__":
    data_to_db(database="encar", table_name=["info", "faq"])
