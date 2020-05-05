import os
import re
import logging
from flask import Flask, g, session
from flask_migrate import Migrate
from web.api.routes import api
from web.api.account_routes import account
from web.api.address_routes import address
from flask_sqlalchemy import SQLAlchemy
from .database import db, Base
from .auth import *
import inspect

logger = logging.getLogger(__name__)

def camelize_classname(base, tablename, table):
    "Produce a 'camelized' class name, e.g. "
    "'words_and_underscores' -> 'WordsAndUnderscores'"
    return str(tablename[0].upper() + \
            re.sub(r'_([a-z])', lambda m: m.group(1).upper(), tablename[1:]))


def register_extensions(app):
    """
    Function to register all extensions
    """
    auth.oauth.init_app(app)
    auth.auth0 = auth.oauth.register(
        'auth0',
        client_id='6s0USrL78smCn92sPwDt6m5ezfiq1sIG',
        client_secret='ti0eaqYemFhWpzGkbvFPFKnn54CXKbN1tX2T9gRr4GPsh84O4OAnWuKWewOS45Zs',
        api_base_url='https://patdeguz.auth0.com',
        access_token_url='https://patdeguz.auth0.com/oauth/token',
        authorize_url='https://patdeguz.auth0.com/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    db.app = app
    db.init_app(app)

def create_app(config_name):
    # create app instance
    app = Flask(__name__)
    # add configuration
    app.config.from_object(config_name)
    # app.logger.setLevel(logging.DEBUG)
    app.logger.info(os.environ)
    app.logger.info(app.config)


    # register extensions
    register_extensions(app)
    # db.app = app
    # db.init_app(app)

    Base.prepare(db.engine, reflect=True)

    # Migrate(app, db)

    # # importing the models to make sure they are known to Flask-Migrate
    # from web.models.user import User
    # from web.models.orders import OrderTable

    # register blueprints
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(account, url_prefix='/account')
    app.register_blueprint(address, url_prefix='/address')

    return app

