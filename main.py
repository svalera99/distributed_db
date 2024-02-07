import sys
from typing import Dict

import argparse
import yaml
from loguru import logger

from experiments.experiments import no_lock_counter, \
                    pessimistic_lock, \
                    optimistic_lock, \
                    atomic_long
from experiments.utils import execute_threads, \
                    reset_map_key, \
                    reset_atomic_long


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg_p", '-c', default="config.yaml", help="Path to cfg")
    return vars(parser.parse_args())

def init_logger(logger_level: str):
    logger.remove()
    logger.add(sys.stdout, level=logger_level)
    logger.add("logs/app_logs.log", level=logger_level, backtrace=True, diagnose=True)


def main(cfg: Dict):
    hazelcast_cfg = cfg["hazelcast"]

    # Experiments
    reset_map_key(hazelcast_cfg)
    execute_threads(no_lock_counter, hazelcast_cfg)

    reset_map_key(hazelcast_cfg)
    execute_threads(pessimistic_lock, hazelcast_cfg)

    reset_map_key(hazelcast_cfg)
    execute_threads(optimistic_lock, hazelcast_cfg)

    reset_atomic_long(hazelcast_cfg)
    execute_threads(atomic_long, hazelcast_cfg)


if __name__ == "__main__":
    cfg = parse_args()

    with open(cfg["cfg_p"]) as file:
        cfg = yaml.safe_load(file)

    init_logger(cfg["logger"]["level"])
    
    main(cfg)