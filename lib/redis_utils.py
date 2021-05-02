from typing import Optional
import redis

from settings import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def set_car(car_cat: str, car_name: str, car_number: str) -> None:
    """lpush key to redis queue

    :param car_cat: car category
    :param car_name: car name
    :param car_number: the car number, ex. WET987 as a value in
                       the relevant redis queue
    """
    key = get_redis_car_key(car_cat, car_name)
    redis_client.lpush(key, car_number)


def get_car(car_cat: str, car_name: str) -> Optional[str]:
    """rpop key from redis queue

    :param car_cat: car category
    :param car_name: car name
    :return: the car number popped from the queue
    """
    key = get_redis_car_key(car_cat, car_name)
    return redis_client.rpop(key)


def get_redis_car_key(car_cat: str, car_name: str) -> str:
    """Generate key by car category and car name

    :param car_cat:
    :param car_name:
    :return: the redis string key
    """
    return f"{car_cat}:{car_name}"


def flush() -> None:
    """from all keys in redis"""
    redis_client.flushall()
