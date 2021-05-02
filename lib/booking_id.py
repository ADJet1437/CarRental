import random
from datetime import datetime


class BookingId:
    sep = '-'

    @staticmethod
    def unique(cus_name: str) -> str:
        """Generate unique booking id

        :param cus_name: customer name
        :return: booking id
        """
        base_str = BookingId._base_str()
        random_str = BookingId._random_str(cus_name)
        return base_str + BookingId.sep + random_str

    @staticmethod
    def _base_str() -> str:
        return datetime.now().strftime("%Y%m%d%H%M%S")

    @staticmethod
    def _random_str(cus_name: str) -> str:
        """Get the random string by the provided customer name

        :param cus_name: customer name
        :return: 4 chars random string from customer name
        """
        cus_name = cus_name.replace(" ", "")
        chars = [random.choice(cus_name).upper() for _ in range(4)]
        return "".join(chars)
