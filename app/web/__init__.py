import os
import re
import logging
from flask import Flask, g, session
from flask_migrate import Migrate
from web.api.routes import api
from web.api.account_routes import account
from web.api.address_routes import address
from web.api.address_type_routes import address_type
from web.api.organization_routes import organization
from web.api.organization_type_routes import organization_type
from web.api.supplier_routes import supplier
from web.api.person_routes import person
from web.api.person_account_routes import person_account
from web.api.restaurant_routes import restaurant
from flask_sqlalchemy import SQLAlchemy
from .database import db, Base
from .auth import *
import inspect
from flask_cors import CORS

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
    auth_base_url = os.environ.get('AUTH0_BASE_URL', 'https://dev-zappotrack.auth0.com')
    auth.oauth.init_app(app)
    auth.auth0 = auth.oauth.register(
        'auth0',
        client_id=os.environ.get('AUTH0_CLIENT_ID'),
        client_secret=os.environ.get('AUTH0_CLIENT_SECRET'),
        api_base_url=auth_base_url,
        access_token_url=f'{auth_base_url}/oauth/token',
        authorize_url=f'{auth_base_url}/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    db.app = app
    db.init_app(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    
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
    app.register_blueprint(address_type, url_prefix='/address_type')
    app.register_blueprint(organization, url_prefix='/organization')
    app.register_blueprint(organization_type, url_prefix='/organization_type')
    app.register_blueprint(supplier, url_prefix='/supplier')
    app.register_blueprint(person, url_prefix='/person')
    app.register_blueprint(person_account, url_prefix='/person_account')
    app.register_blueprint(restaurant, url_prefix='/restaurant')

    return app

