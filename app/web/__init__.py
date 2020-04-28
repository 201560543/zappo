import os
import re
from flask import Flask, g
from flask_migrate import Migrate
from web.api.routes import api
from web.api.account_routes import account
from flask_sqlalchemy import SQLAlchemy
from .database import db, Base

def camelize_classname(base, tablename, table):
    "Produce a 'camelized' class name, e.g. "
    "'words_and_underscores' -> 'WordsAndUnderscores'"
    return str(tablename[0].upper() + \
            re.sub(r'_([a-z])', lambda m: m.group(1).upper(), tablename[1:]))


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
    db.app = app
    db.init_app(app)
    Base.prepare(db.engine, reflect=True, classname_for_table=camelize_classname)
    # Migrate(app, db)

    # # importing the models to make sure they are known to Flask-Migrate
    # from web.models.user import User
    # from web.models.orders import OrderTable

    # register blueprints
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(account, url_prefix='/account')


    return app


