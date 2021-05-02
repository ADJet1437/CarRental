from application import app
from views.car import register_view, car_return_view, car_cancel_view
from settings import URL_PREFIX


# Car Blueprints
app.register_blueprint(register_view, url_prefix=URL_PREFIX)
app.register_blueprint(car_return_view, url_prefix=URL_PREFIX)
app.register_blueprint(car_cancel_view, url_prefix=URL_PREFIX)
