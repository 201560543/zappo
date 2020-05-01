import json
import request
from . import account
from web.models.account import Account
from web.api.api_utils import converter, exception_handler
from web.database import db
from flask import current_app

@account.app_errorhandler(404)
def page_not_found(e):
    current_app.logger.warn(f'404 not found')
    current_app.logger.warn(e)
    return 'Account API not Found', 404

@account.app_errorhandler(500)
def server_error(e):
    current_app.logger.warn('500 internal server error')
    current_app.logger.warn(e)
    return '500 Internal Server Error', 500

@account.route('/', methods=['GET'])
@exception_handler(custom_msg='Issues in fetching')
def get_all_accounts(return_json=True):
    results = db.session.query(Account).all()
    result_dicts = [acnt.as_dict() for acnt in results]
    current_app.logger.info(result_dicts)
    if return_json == True:
        return json.dumps(result_dicts, default=converter)
    else:
        return result_dicts

@account.route('/<int:account_number>/', methods=['GET'])
@exception_handler()
def get_account_by_account_number(account_number, return_json=True):
    results = db.session.query(Account).filter_by(account_number=account_number).all()
    result_dicts = [acnt.as_dict() for acnt in results]
    current_app.logger.info(result_dicts)
    if return_json == True:
        return json.dumps(result_dicts, default=converter)
    else:
        return result_dicts
