import os


# URI settings and management
URL_PREFIX = "/api"
API_VERSION = {"v1": "/v1"}
REGISTER_PATH_V1 = API_VERSION["v1"] + "/register"
RETURN_PATH_V1 = API_VERSION["v1"] + "/return"
CANCEL_PATH_V1 = API_VERSION["v1"] + "/cancel"

# database settings
REDIS_HOST = "redis"
REDIS_PORT = 6379
MYSQL_HOST = "mysql"
MYSQL_PORT = "3306"
MYSQL_DB = "test"
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PWD = os.environ.get("MYSQL_PWD")
MYSQL_DB_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# Price settings
BASE_DAY_RENTAL = 50
KILOMETER_PRICE = 10
PREMIUM_BASE_DAY_COEFFICIENT = 1.2
MINIVAN_BASE_DAY_COEFFICIENT = 1.7
MINIVAN_BASE_DISTANCE_COEFFICIENT = 1.5

# Response message settings
BAD_PARAMETER = "Bad parameter"
BOOKING_NOT_FOUND = "Booking reference not found"
BOOKING_RETURNED = "Booking has already returned"
CAR_NOT_AVAILABLE = "Car not available"
CAR_NOT_EXIST = "Car not found"
CAN_NOT_CANCEL = "You can only cancel the booking in 15 minutes after registered"

# Other settings
TIME_LIMIT_TO_CANCEL = 900  # 15 minutes to cancel after registered
