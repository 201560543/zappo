from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app(config_name):
    # create app instance
    app = Flask(__name__)

    # add configuration
    app.config.from_object(config_name)

    # register extensions
    # db.app = app
    db.init_app(app)
    Migrate(app, db)

    # importing the models to make sure they are known to Flask-Migrate
    from web.models.user import User

    return app

