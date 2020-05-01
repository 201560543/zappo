from . import account
from web.models.account import Account
from web.api.api_utils import converter
from web.database import db
from flask import current_app
import json

@account.route('/', methods=['GET'])
def get_all_accounts(return_json=True):
    # TO DO: Add error handling
    results = db.session.query(Account).all()
    result_dicts = [acnt.as_dict() for acnt in results]
    current_app.logger.info(result_dicts)
    
    if return_json == True:
        return json.dumps(result_dicts, default=converter)
    else:
        return result_dicts

@account.route('/<account_number>', methods=['GET'])
def get_account_by_account_number(account_number, return_json=True):
    # TO DO: Add error handling
    results = db.session.query(Account).filter_by(account_number=account_number).all()
    result_dicts = [acnt.as_dict() for acnt in results]
    current_app.logger.info(result_dicts)
    if return_json == True:
        return json.dumps(result_dicts, default=converter)
    else:
        return result_dicts
