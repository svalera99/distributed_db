from loguru import logger

from experiments.utils import create_client, set_key_to_value
from experiments.value_wrapper import ValueWrapper


def no_lock_counter(hazelcast_cfg):
    client = create_client(hazelcast_cfg)
    map = client.get_map(hazelcast_cfg["map"]["name"]).blocking()
    if not map.contains_key(hazelcast_cfg["map"]["key"]):
        map.set(hazelcast_cfg["map"]["key"], 0)

    for _ in range(10000):
        value = map.get(hazelcast_cfg["map"]["key"])
        map.set(hazelcast_cfg["map"]["key"], value + 1)

    client.shutdown()


def pessimistic_lock(hazelcast_cfg):
    client = create_client(hazelcast_cfg)
    distributed_map = client.get_map(hazelcast_cfg["map"]["name"]).blocking()

    set_key_to_value(distributed_map, hazelcast_cfg, 0)

    for _ in range(10000):
        distributed_map.lock(hazelcast_cfg["map"]["key"])
        try:
            value = distributed_map.get(hazelcast_cfg["map"]["key"])
            value += 1
            distributed_map.put(hazelcast_cfg["map"]["key"], value)
        finally:
            distributed_map.unlock(hazelcast_cfg["map"]["key"])
    client.shutdown()


def optimistic_lock(hazelcast_cfg):
    client = create_client(hazelcast_cfg)
    distributed_map = client.get_map(hazelcast_cfg["map"]["name"]).blocking()

    set_key_to_value(distributed_map, hazelcast_cfg, ValueWrapper())

    for _ in range(10000):
        while True:
            old_value = distributed_map.get(hazelcast_cfg["map"]["key"])
            new_value = ValueWrapper(old_value)
            new_value.val += 1
            if distributed_map.replace_if_same(hazelcast_cfg["map"]["key"], old_value, new_value):
                break
    client.shutdown()


def atomic_long(hazelcast_cfg):
    client = create_client(hazelcast_cfg)
    counter_instance = client.cp_subsystem.get_atomic_long(hazelcast_cfg["map"]["key"]).blocking()

    for _ in range(10000):
        counter_instance.increment_and_get()
    client.shutdown()
