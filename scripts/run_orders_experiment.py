import sys

from loguru import logger

from cassandra.cluster import Cluster

def init_logger(logger_level: str, log_file_name: str):
    logger.remove()
    logger.add(sys.stdout, level=logger_level)
    logger.add(f"results/{log_file_name}.log", level=logger_level, backtrace=True, diagnose=True)



if __name__ == "__main__":
    init_logger("INFO", "orders")

    cluster = Cluster(['cassandra'], port=9042).connect("items")

    # Task 1
    logger.info(f'Task 1. Structure of the table - {cluster.execute("DESCRIBE orders;").all()}')

    # Task 2 
    cmnd = "SELECT * from orders WHERE customer_name='Valery Pupkin' ORDER BY order_date"
    logger.info(f'Task 2. All order of Valery Pupkin sorted by date - {cluster.execute(cmnd).all()}')

    # Task 3
    cmnd = "SELECT * from orders WHERE customer_name='Valery Pupkin' AND items_ids CONTAINS 480881;"
    logger.info(f'Task 3. All orders of Valery Pupkin that have item with id 480881 - {cluster.execute(cmnd).all()}')

    # Task 4
    cmnd = "SELECT * FROM orders WHERE customer_name = 'Valery Pupkin' AND order_date >= '2010-10-10';"
    logger.info(f'Task 4.1 All rows for Valery Pupkin and date more than 2010-10-10 {cluster.execute(cmnd).all()}')

    cmnd = "SELECT COUNT(*) FROM orders WHERE customer_name = 'Valery Pupkin' AND order_date >= '2010-10-10';"
    logger.info(f'Task 4.2 Number of rows for Valery Pupkin and date more than 2010-10-10 {cluster.execute(cmnd).all()}')

    # Task 5
    cmnd = "SELECT order_price FROM orders WHERE customer_name = 'Valery Pupkin';"
    logger.info(f'Task 5 Sum of every order of Valery Pupkin {cluster.execute(cmnd).all()}')


    # Task 8
    cmnd = "SELECT WRITETIME(order_price) FROM orders WHERE customer_name = 'Valery Pupkin';"
    logger.info(f'Task 8. Writetime for all orders {cluster.execute(cmnd).all()}')


    # Task 9
    cmnd = "INSERT INTO orders (customer_name, order_date, items_ids, order_price) VALUES ('Valery Dupin', '2024-10-10', [23123123, 23123123], 1000) USING TTL 86400;"
    logger.info(f'Task 9 Creating row with some TTL {cluster.execute(cmnd).all()}')