from lib.booking_id import BookingId


def test_unique_booking_id():
    customer_name = "Customer"
    unique_id_1 = BookingId.unique(customer_name)
    unique_id_2 = BookingId.unique(customer_name)
    assert unique_id_1 != unique_id_2
