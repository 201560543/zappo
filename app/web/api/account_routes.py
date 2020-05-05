import json
from . import account
from web.models.account import Account
from web.api.api_utils import converter, exception_handler
from web.database import db
from flask import current_app, request, jsonify
import uuid
from datetime import datetime as dt

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

@account.route('/create', methods=['POST'])
@exception_handler()
def create_account(return_json=True):
    body={}
    data = request.get_json()

    org_id = data.get('organization_id')
    addr_id = data.get('address_id')
    accnt_num = uuid.uuid1().hex # Setting account number
    accnt_name = data.get('account_name')
    tz_name = data.get('timezone_name')

    # Creating new address
    new_accnt = Account(
        organization_id=org_id,
        address_id=addr_id,
        account_number=accnt_num,
        account_name=accnt_name,
        created_at=dt.now(),
        timezone_name=tz_name
    )
    body['obj']=new_accnt.as_dict()

    db.session.add(new_accnt)
    db.session.commit()
    current_app.logger.info('Inserted record:\n',new_accnt)
    db.session.close()
    body['success']=True
    return json.dumps(body, default=converter)
