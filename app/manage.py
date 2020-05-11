from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from web import create_app, db
from web.config import base

app = create_app(base)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    from web.models.user import User
    from web.models.orders import Order
    from web.models.order_items import OrderItem
    from web.models.account import Account
    from web.models.supplier import Supplier
    # To do, run this to get new tables
    from web.models.person import Person
    from web.models.person_account import PersonAccount
    from web.models.restaurant import Restaurant
    manager.run()