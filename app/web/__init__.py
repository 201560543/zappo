import os
import re
import logging
from flask import Flask, g
from flask_migrate import Migrate
from web.api.routes import api
from flask_sqlalchemy import SQLAlchemy
from .database import db, Base

logger = logging.getLogger(__name__)

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
    app.logger.setLevel(logging.DEBUG)
    app.logger.info(os.environ)
    app.logger.info(app.config)

    # register extensions
    db.app = app
    db.init_app(app)

    Base.prepare(db.engine, reflect=True)

    # Migrate(app, db)

    # # importing the models to make sure they are known to Flask-Migrate
    # from web.models.user import User
    # from web.models.orders import OrderTable

    # register blueprints
    app.register_blueprint(api, url_prefix='/api')


    return app


