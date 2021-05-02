import json

from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from settings import MYSQL_DB_URI, REGISTER_PATH_V1, RETURN_PATH_V1, CANCEL_PATH_V1, URL_PREFIX


app = Flask("CarRental")
app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.before_request
def process_request():
    """A middleware to verify all needed parameters in endpoints"""
    app.logger.info("Processing request")
    try:
        data = json.loads(request.data)
    except json.decoder.JSONDecodeError:
        # In case data is not in proper json format
        abort(400)
    if request.path == URL_PREFIX + REGISTER_PATH_V1:
        if not (
            data.get("name")
            and data.get("car_category")
            and data.get("customer")
            and data.get("birthday")
            and data.get("rental_days")
        ):
            abort(400)
    elif request.path == URL_PREFIX + RETURN_PATH_V1:
        if not (data.get("booking_id") and data.get("mileage")):
            abort(400)
    elif request.path == URL_PREFIX + CANCEL_PATH_V1:
        if not data.get("booking_id"):
            abort(400)
