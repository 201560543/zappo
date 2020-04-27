import os
from flask import Flask, g
from flask_migrate import Migrate
from web.api.routes import api
from .database import db

def create_app(config_name):
    # create app instance
    app = Flask(__name__)

    # add configuration
    app.config.from_object(config_name)
    
    # Check if the env exists
    host = os.environ.get('DB_HOST')
    if host:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@{host}/'
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


