import json
from datetime import datetime

from flask import Blueprint, request, jsonify

from application import db, app
from models import Car, Booking
from lib.booking_id import BookingId
from lib.price_calculator import PriceHandler
from lib.redis_utils import get_car, set_car
from settings import CAR_NOT_AVAILABLE, BOOKING_NOT_FOUND, BOOKING_RETURNED,CAN_NOT_CANCEL,\
    TIME_LIMIT_TO_CANCEL, CAR_NOT_EXIST, BAD_PARAMETER, REGISTER_PATH_V1, RETURN_PATH_V1, CANCEL_PATH_V1


register_view = Blueprint("register_view", __name__)
car_return_view = Blueprint("car_return_view", __name__)
car_cancel_view = Blueprint("car_cancel_view", __name__)


@register_view.route(REGISTER_PATH_V1, methods=["POST"])
def register():
    """Register a car"""
    data = json.loads(request.data)

    car_number = get_car(data["car_category"], data["name"])
    if car_number is None:
        # Currently this type of car not available
        return {"status": CAR_NOT_AVAILABLE}

    app.logger.info(f"Processing car number: {car_number}")

    car = Car.query.filter_by(
        name=data['name'], category=data["car_category"], number=car_number
    ).first()
    if not car:
        return {"failure": CAR_NOT_EXIST}, 404

    # Generate the booking reference
    booking = Booking()
    booking.booking_id = BookingId.unique(data["customer"])
    booking.customer = data["customer"]
    booking.customer_birthday = data["birthday"]
    booking.booking_car_id = car.id
    booking.booking_car_category = data["car_category"]
    booking.rental_days = data["rental_days"]
    booking.mileage_at_pickup = car.mileage
    booking.booking_date = datetime.now()
    car.available = False
    db.session.add(booking)
    db.session.commit()

    # Response and logging
    resp = booking.get_register_info()
    resp.update(car.get_car_info())
    app.logger.info(f"Successfully registered, info: {resp}")

    return jsonify(resp)


@car_return_view.route(RETURN_PATH_V1, methods=["POST"])
def car_return():
    """Return a car"""
    data = json.loads(request.data)
    mileage = data["mileage"]

    booking = Booking.query.filter_by(booking_id=data["booking_id"]).first()

    # Wrong booking id
    if not booking:
        return {"failure": BOOKING_NOT_FOUND}, 404

    # In case duplicate return
    if booking.returned:
        return {"status": BOOKING_RETURNED}, 202

    car = db.session.query(Car).filter_by(id=booking.booking_car_id).first()

    # check if mileage is reasonable
    if mileage < car.mileage:
        return {"failure": BAD_PARAMETER}, 400

    now = datetime.now()

    # In case return later than the booking rental days
    started_datetime = booking.booking_date
    delta = now - started_datetime
    days = booking.rental_days
    if delta.days > booking.rental_days:
        days = delta.days

    # Calculate price
    used_mileage = mileage - booking.mileage_at_pickup
    price_handler = PriceHandler(
        category=booking.booking_car_category,
        days=days,
        used_mileage=used_mileage
    )
    price = price_handler.calculate()

    # update booking
    booking.price = price
    booking.rental_days = days
    booking.mileage_at_return = mileage
    booking.returned = True
    booking.return_date = now
    # update car availability
    car.available = True
    db.session.commit()
    # produce car to redis queue for next time to consume
    set_car(car.category, car.name, car.number)

    resp = booking.get_return_info()
    app.logger.info(f"Successfully returned, info: {resp}")

    return jsonify(resp)


@car_cancel_view.route(CANCEL_PATH_V1, methods=["POST"])
def cancel():
    """Cancel the booking by the provided booking id,
    only within 15 minutes then can be canceled
    """
    data = json.loads(request.data)
    booking_id = data["booking_id"]
    booking = Booking.query.filter_by(booking_id=booking_id).first()

    if not booking:
        return {"status": BOOKING_NOT_FOUND}, 404

    if booking.returned:
        return {"status": BOOKING_RETURNED}, 202

    delta = datetime.now() - booking.booking_date
    if delta.seconds > TIME_LIMIT_TO_CANCEL:
        return {"failure": CAN_NOT_CANCEL}

    booking.returned = True
    car = Car.query.filter_by(id=booking.booking_car_id).first()
    car.available = True
    db.session.commit()
    set_car(car.category, car.name, car.number)

    resp = booking.get_cancel_info()
    app.logger.info(f"Successfully canceled, info: {resp}")

    return jsonify(resp)
