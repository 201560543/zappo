from datetime import datetime, date
from functools import wraps
from flask import current_app, abort

def converter(obj):
    """
    Used to convert an object into a json-serializable representation for api calls
    """
    if isinstance(obj, datetime):
        return obj.__str__()
    elif isinstance(obj, date):
        return obj.__str__()


def exception_handler(**kw):
    """
    Function to handle all code errors and logs for us. This function also takes
    keyword arguments. If you want to add more arguments here then make sure to check for
    them as show below:
    Arguments:
    kw: (keyword argumets) {
        'custom_msg': ''
    }
    """
    custom_msg = kw.get('custom_msg', 'Found an exception while making a request')
    def handler(func):
        """
        Main function wrapper
        """
        @wraps(func)
        def inner(*args, **kwargs):
            """
            Inner function to log all issues
            """
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                current_app.logger.warn(custom_msg)
                current_app.logger.warn(exc)
                abort(400, description='Kindly contact your dev team to handle this error')
        return inner
    return handler