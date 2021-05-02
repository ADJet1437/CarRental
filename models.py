from application import db


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(8), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
    mileage = db.Column(db.Float, nullable=False)

    def get_car_info(self):
        return {
            "name": self.name,
            "nr": self.number,
            "category": self.category
        }


class Booking(db.Model):
    booking_id = db.Column(db.String(20), primary_key=True)
    customer = db.Column(db.String(30), nullable=False)
    customer_birthday = db.Column(db.Date, nullable=False)
    booking_car_id = db.Column(db.Integer, nullable=False)
    booking_car_category = db.Column(db.String(30), nullable=False)
    mileage_at_pickup = db.Column(db.Float, nullable=False)
    mileage_at_return = db.Column(db.Float)
    booking_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime)
    rental_days = db.Column(db.Integer, nullable=False)
    returned = db.Column(db.Boolean, nullable=False, default=False)
    price = db.Column(db.Float)

    def get_register_info(self):
        return {
            "booking_id": self.booking_id,
            "customer": {
                "name": self.customer,
                "birthday": self.customer_birthday.strftime("%Y-%m-%d")
            },
            "rental": {
                "start_date": self.booking_date.strftime("%Y-%m-%d"),
                "rental_days": self.rental_days
            }
        }

    def get_return_info(self):
        return {
            "booking_id": self.booking_id,
            "status": "success",
            "car": {
                "category": self.booking_car_category,
                "current_mileage": self.mileage_at_return,
                "used_mileage": self.mileage_at_return - self.mileage_at_pickup
            },
            "total_price": self.price
        }

    def get_cancel_info(self):
        return {
            "booking_id": self.booking_id,
            "status": "Canceled"
        }
