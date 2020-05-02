import json
from . import account
from web.models.account import Account
from web.api.api_utils import converter, exception_handler
from web.database import db
from flask import current_app

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

@account.route('/<account_number>', methods=['GET'])
@exception_handler()
def get_account_by_account_number(account_number, return_json=True):
    result = db.session.query(Account).filter_by(account_number=account_number).one_or_none()
    result_dict = result.as_dict()
    current_app.logger.info(result_dict)
    if return_json == True:
        return json.dumps(result_dict, default=converter)
    else:
        return result_dict
