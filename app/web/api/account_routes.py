from . import account
from web.models.account import Account
from web.api.api_utils import converter
from web.database import db
import json

@account.route('/accounts', methods=['GET'])
def get_all_accounts(return_json=True):
    results = db.session.query(Account).all()
    result_dicts = [acnt.as_dict() for acnt in results]
    if return_json == True:
        return json.dumps(result_dicts, default=converter)
    else:
        return result_dicts
        
@account.route('/accounts/<account_number>', methods=['GET'])
def get_account_by_account_number(account_number, return_json=True):
    results = db.session.query(Account).filter_by(account_number=account_number).all()
    result_dicts = [acnt.as_dict() for acnt in results]
    if return_json == True:
        return json.dumps(result_dicts, default=converter)
    else:
        return result_dicts
