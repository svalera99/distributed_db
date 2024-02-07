from time import time
from functools import wraps
from multiprocessing import Process
from typing import Callable, Dict
import sys

from loguru import logger
import yaml
import psycopg2


def init_logger(logger_level: str):
    logger.remove()
    logger.add(sys.stdout, level=logger_level)
    logger.add("results.log", level=logger_level, backtrace=True, diagnose=True)

def create_conn_cursor(args):
    postgres_args = args["postgres"]
    conn = psycopg2.connect(database=postgres_args["db_name"],
                        host=postgres_args["host"],
                        user=postgres_args["user"],
                        password=postgres_args["password"],
                        port=postgres_args["port"])
    cursor = conn.cursor()
    return conn, cursor

def measure_time(f):
    @wraps(f)
    def wrapper(*args, **kw):
        logger.info(f"{'-'*30}")
        logger.info(f"Starting measuring function {args[0].__name__}")
        was = time()
        f(*args, **kw)
        logger.info(f"Function laster for {time() - was}")
        logger.info(f"Function {f.__name__} DONE")
        logger.info(f"{'*'*30}")

    return wrapper

@measure_time
def execute_threads(worker_function: Callable, args: Dict):
    processes = []
    for _ in range(10):
        p = Process(target=worker_function, args=(args,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    _, cursor = create_conn_cursor(args)
    cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1")
    total_likes = cursor.fetchone()[0]
    logger.info(f"There were total of {total_likes}")

def cleanup_the_row(args):
    conn, cursor = create_conn_cursor(args)
    cursor.execute(f"update user_counter set counter = 0 where user_id = 1")
    conn.commit()

# actual scenarious

def lost_update(args):
    conn, cursor = create_conn_cursor(args)
    for _ in range(10000):
        cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1")
        counter = cursor.fetchone()[0]
        counter = counter + 1
        cursor.execute(f"update user_counter set counter = {counter} where user_id = 1")
        conn.commit()

def in_place_update(args):
    conn, cursor = create_conn_cursor(args)
    for _ in range(10000):
        cursor.execute("update user_counter set counter = counter + 1 where user_id = 1")
        conn.commit()

def row_level_locking(args):
    conn, cursor = create_conn_cursor(args)
    for _ in range(10000):
        cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1 FOR UPDATE")
        counter = cursor.fetchone()[0]
        counter = counter + 1
        cursor.execute(f"update user_counter set counter = {counter} where user_id = 1")
        conn.commit()

def optimistic_concurrency_control(args):
    conn, cursor = create_conn_cursor(args)
    for _ in range(10000):
        while True:
            cursor.execute("SELECT counter, version FROM user_counter WHERE user_id = 1")
            counter, version = cursor.fetchone()
            counter += 1
            cursor.execute(
                f"update user_counter set counter = {counter}, version = {version + 1} "
                f"where user_id = 1 and version = {version}"
            )
            conn.commit()
            if cursor.rowcount > 0:
                break


if __name__ == "__main__":
    with open("args.yaml") as f:
        args = yaml.safe_load(f)

    init_logger("INFO")

    for func in [lost_update, in_place_update, row_level_locking, optimistic_concurrency_control]:
        cleanup_the_row(args)
        execute_threads(func, args)
