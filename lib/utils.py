import sqlalchemy

from settings import MYSQL_DB_URI
from lib.redis_utils import set_car, flush


engine = sqlalchemy.create_engine(MYSQL_DB_URI)


def insert_cars() -> None:
    """Prepare some data samples (cars) to MySQL"""
    query = """
        INSERT INTO test.car(name, number, category, available, mileage)
        VALUES  ("Audi A5", "BEW345", "premium", true, 212.6),
                ("Audi A3", "WWW457", "compact", true, 175.4),
                ("Audi A3", "OPD557", "compact", true, 145.4),
                ("BMW X1", "RTW555", "compact", true, 155.4),
                ("Audi A7", "NMN234", "premium", true, 123.7),
                ("Volvo S9", "BUE325", "premium", true, 314.5),
                ("Volvo S9", "BVE355", "premium", true, 344.5),
                ("Volvo S9", "BUR724", "premium", true, 124.5),
                ("Volvo S9", "BHH727", "premium", true, 234.5),
                ("Mercedes benz vito", "IYG989", "minivan", true, 93);
    """
    with engine.connect() as conn:
        conn.execute(query)


def load_redis() -> None:
    """SELECT cars which are available
     and load them in Redis queue.
     """
    query = """
        SELECT
            name,
            category,
            number
        FROM test.car
        WHERE available = 1
    """
    with engine.connect() as conn:
        cars = list(conn.execute(query))

    for car in cars:
        set_car(car["category"], car["name"], car["number"])
