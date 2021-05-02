from flask_script import Command, Manager, Server

from blueprints import app


manager = Manager(app)


@Command
def create_models():
    """Map all models to database"""
    from application import db
    db.create_all()


@Command
def load_data():
    """Prepare data, including MySQL and Redis"""
    from lib.utils import insert_cars, load_redis
    insert_cars()
    load_redis()


@Command
def flush_keys():
    from lib.redis_utils import flush
    flush()


# Map function to command
manager.add_command("create_tables", create_models)
manager.add_command("load_data", load_data)
manager.add_command("flush_redis_keys", flush_keys)
manager.add_command(
    "runserver",
    Server(host='0.0.0.0', use_reloader=True, use_debugger=True)
)


def run():
    manager.run()


if __name__ == '__main__':
    run()
