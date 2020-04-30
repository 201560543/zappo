# flake8: noqa
import os
from .env import ENV_BOOL, ENV_STR, ABS_PATH

DEBUG = ENV_BOOL('DEBUG', False)
SECRET_KEY = ENV_STR('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root@localhost/zappo_main'
SQLALCHEMY_TRACK_MODIFICATIONS = True

if os.environ.get('MYSQL_DB_BIND') and os.environ.get('MEMSQL_DB_BIND'):
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/binds/
    SQLALCHEMY_DATABASE_URI = os.environ.get('MYSQL_DB_BIND')
    SQLALCHEMY_BINDS = {
        'mysql_db': os.environ.get('MYSQL_DB_BIND'),
        'memsql_db': os.environ.get('MEMSQL_DB_BIND')
    }