from functools import wraps
from time import time
from multiprocessing import Process
from typing import Callable, Dict

from loguru import logger
import hazelcast

def measure_time(f):
    @wraps(f)
    def wrapper(*args, **kw):
        logger.info(f"{'-'*30}")
        func_name = args[0].__name__
        logger.info(f"Starting measuring function {func_name}")
        was = time()
        f(*args, **kw)
        logger.info(f"Function laster for {time() - was}")
        logger.info(f"Function {func_name} DONE")

        hazelcast_cfg = args[1]
        client = create_client(hazelcast_cfg)
        if func_name != "atomic_long":
            map = client.get_map(hazelcast_cfg["map"]["name"]).blocking()
            logger.info(
                f"Value of {hazelcast_cfg['map']['key']} at "
                f"the end of function is {map.get(hazelcast_cfg['map']['key'])}"
            )
        else:
            counter_instance = client.cp_subsystem.get_atomic_long(hazelcast_cfg["map"]["key"]).blocking()
            logger.info(
                f"Value of {hazelcast_cfg['map']['key']} at "
                f"the end of function is {counter_instance.get()}"
            )

        logger.info(f"{'*'*30}")

    return wrapper

@measure_time
def execute_threads(
    worker_function: Callable,
    hazelcast_cfg: Dict
):
    processes = []
    for _ in range(10):
        p = Process(target=worker_function, args=(hazelcast_cfg,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

def create_client(hazelcast_cfg: Dict):
    return hazelcast.HazelcastClient(
        cluster_name=hazelcast_cfg["cluster_name"],
        cluster_members=hazelcast_cfg["cluster_members"]
    )

def reset_map_key(hazelcast_cfg):
    client = create_client(hazelcast_cfg)
    map = client.get_map(hazelcast_cfg["map"]["name"]).blocking()
    map.delete(hazelcast_cfg["map"]["key"])

def set_key_to_value(map, hazelcast_cfg, value):
    map.lock(hazelcast_cfg["map"]["key"])
    if not map.contains_key(hazelcast_cfg["map"]["key"]):
        map.set(hazelcast_cfg["map"]["key"], value)
    map.unlock(hazelcast_cfg["map"]["key"])

def reset_atomic_long(hazelcast_cfg):
    client = create_client(hazelcast_cfg)
    counter_instance = client.cp_subsystem.get_atomic_long(hazelcast_cfg["map"]["key"]).blocking()
    counter_instance.set(0)
    client.shutdown()