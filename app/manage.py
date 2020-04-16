from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from web import create_app, get_db
from web.config import base

app = create_app(base)
db = get_db()

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    from web.models.user import User
    from web.models.orders import Order
    from web.models.order_items import OrderItem
    manager.run()