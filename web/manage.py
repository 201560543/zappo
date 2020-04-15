from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from init import create_app, db
from config import base

app = create_app(base)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()