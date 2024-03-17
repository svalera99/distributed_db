import sys

from loguru import logger

from cassandra.cluster import Cluster

def init_logger(logger_level: str, log_file_name: str):
    logger.remove()
    logger.add(sys.stdout, level=logger_level)
    logger.add(f"results/{log_file_name}.log", level=logger_level, backtrace=True, diagnose=True)



if __name__ == "__main__":
    init_logger("INFO", "items")

    cluster = Cluster(['cassandra'], port=9042).connect("items")

    # # Task 1
    # logger.info(f'Task 1. Structure of the table - {cluster.execute("DESCRIBE items.items;").all()}')

    # # # Task 2 ORDER BY price
    # cmnd = "SELECT * from items WHERE category='Food' ORDER BY price"
    # logger.info(f'Task 2. All food sorted by price - {cluster.execute(cmnd).all()}')

    # # # Task 3 Choose by criterias
    # # # Task 3.1 choose by name
    # cmnd = "SELECT * from items_by_category_model WHERE category='Food' AND model='Model A'"
    # logger.info(f'Task 3.1 All food with model = Model A - {cluster.execute(cmnd).all()}')

    # # # Task 3.2 
    # cmnd = "SELECT * from items WHERE category='Food' AND price > 100 AND price < 500"
    # logger.info(f'Task 3.2 All food with 100 < price < 500 - {cluster.execute(cmnd).all()}')

    # # # Task 3.3
    # cmnd = "SELECT * from items_by_category_model WHERE category='Food' AND price = 833.74 AND model = 'Model C'"
    # logger.info(f'Task 3.3 All food with price = 833.74 and model = Model C  - {cluster.execute(cmnd).all()}')

