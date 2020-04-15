from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app(config_name):
    # create app instance
    print(__name__)
    app = Flask(__name__)

    # add configuration
    app.config.from_object(config_name)

    # register extensions
    db.app = app
    db.init_app(app)

    return app

