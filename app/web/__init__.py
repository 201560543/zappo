from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from web.api.routes import api

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        #Make sure that the arguments correspond to your current MemSQL instance.
        db = g._database = SQLAlchemy()


def create_app(config_name):
    # create app instance
    app = Flask(__name__)

    # add configuration
    app.config.from_object(config_name)

    # register extensions
    # db.app = app
    db.init_app(app)
    # Migrate(app, db)

    # # importing the models to make sure they are known to Flask-Migrate
    # from web.models.user import User
    # from web.models.orders import OrderTable

    # register blueprints
    app.register_blueprint(api, url_prefix='/api')


    return app


