# flake8: noqa
import os
from .env import ENV_BOOL, ENV_STR, ABS_PATH

DEBUG = ENV_BOOL('DEBUG', False)
SECRET_KEY = ENV_STR('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root@localhost/zappo'

SQLALCHEMY_TRACK_MODIFICATIONS = True
