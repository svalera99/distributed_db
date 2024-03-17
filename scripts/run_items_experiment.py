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

    # Task 1
    logger.info(f'Task 1. Structure of the table - {cluster.execute("DESCRIBE items.items;").all()}')

    # # Task 2 ORDER BY price
    cmnd = "SELECT * from items WHERE category='Food' ORDER BY price"
    logger.info(f'Task 2. All food sorted by price - {cluster.execute(cmnd).all()}')

    # # Task 3 Choose by criterias
    # # Task 3.1 choose by name
    cmnd = "SELECT * from items_by_category_model WHERE category='Food' AND model='Model A'"
    logger.info(f'Task 3.1 All food with model = Model A - {cluster.execute(cmnd).all()}')

    # # Task 3.2 
    cmnd = "SELECT * from items WHERE category='Food' AND price > 100 AND price < 500"
    logger.info(f'Task 3.2 All food with 100 < price < 500 - {cluster.execute(cmnd).all()}')

    # # Task 3.3
    cmnd = "SELECT * from items_by_category_model WHERE category='Food' AND price = 833.74 AND model = 'Model C'"
    logger.info(f'Task 3.3 All food with price = 833.74 and model = Model C  - {cluster.execute(cmnd).all()}')

    # Task 4
    # Task 4.1
    cmnd = "SELECT * from items WHERE characteristics CONTAINS KEY 'additional_field'"
    logger.info(f'Task 4.1 All entries where map has field additional_field - {cluster.execute(cmnd).all()}')

    # Task 4.2
    cmnd = "SELECT * from items WHERE characteristics['additional_field'] = 'some_field'"
    logger.info(f'Task 4.2 All entries where map\'s field additional_field = some_field - {cluster.execute(cmnd).all()}')

    # Task 5
    # Task 5.1
    cmnd = "UPDATE items SET characteristics['additional_field'] = 'new_value' WHERE category = 'Food' AND price = 833.74"
    cluster.execute(cmnd).all()
    cmnd = "SELECT characteristics from items WHERE category = 'Food' AND price = 833.74"
    logger.info(f'Changing value to new_value - {cluster.execute(cmnd).all()}')

    # Task 5.2
    cmnd = ("UPDATE items SET characteristics = characteristics + {'new_key': 'super_new_values'}"
                    "WHERE category = 'Food' AND price = 833.74")
    cluster.execute(cmnd).all()
    cmnd = "SELECT characteristics from items WHERE category = 'Food' AND price = 833.74"
    logger.info(f'Adding new key-value pair new_key: super_new_values- {cluster.execute(cmnd).all()}')

    # Task 5.3
    cmnd = ("UPDATE items SET characteristics = characteristics - {'new_key'}"
                    "WHERE category = 'Food' AND price = 833.74")
    cluster.execute(cmnd).all()
    cmnd = "SELECT characteristics from items WHERE category = 'Food' AND price = 833.74"
    logger.info(f'Deleted pair new_key: super_new_values- {cluster.execute(cmnd).all()}')