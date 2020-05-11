import json
from . import account
from web.models.account import Account
from web.models.person import Person
from web.models.person_account import PersonAccount
from web.models.restaurant import Restaurant
from web.models.address import Address
from web.api.api_utils import converter, exception_handler
from web.database import db
from flask import current_app, request, jsonify
from .organization_routes import insert_organization
from .address_routes import insert_address
from .person_routes import insert_person
from .person_account_routes import insert_person_account
from .restaurant_routes import insert_restaurant
import uuid
from datetime import datetime as dt

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
    """
    To be deprecated. Instead, new_account should be used
    """
    body={}
    data = request.get_json()

    new_org_id = data.get('organization_id')
    addr_id = data.get('address_id')
    accnt_num = uuid.uuid1().hex # Setting account number
    accnt_name = data.get('account_name')
    tz_name = data.get('timezone_name')

    # Creating new address
    new_accnt = Account(
        organization_id=new_org_id,
        address_id=addr_id,
        account_number=accnt_num,
        account_name=accnt_name,
        created_at=dt.now(),
        timezone_name=tz_name
    )
    body['obj']=new_accnt.as_dict()

    db.session.add(new_accnt)
    import pdb; pdb.set_trace()
    db.session.commit()
    current_app.logger.info('Inserted record:\n',new_accnt)
    db.session.close()
    body['success']=True
    return json.dumps(body, default=converter)

@account.route('/new_account', methods=['POST'])
@exception_handler()
def create_new_account(return_json=True):
    """
    Route to create a brand new account/user. Meant to occur after a user first signs up through authentication service.

    Inserts records into the following tables in the following order:
    1. organization
    2. address (one record for organization "sold to" address and one record for "ship to" address)
    3. account
    4. person
    5. person_account
    6. restaurant
    """
    body = {
        "success":None
        }
    # Fetch Relevant Values
    data = request.get_json()
    dt_now = dt.now()
    # Insert Organization
    new_org = insert_organization(data=data, dt_now=dt_now, add=True, flush=True)
    current_app.logger.info('Inserted record:\n',new_org)
    new_org_number = new_org.organization_number # Fetching organization number of new record
    new_org_id = new_org.id # Fetching organization id of new record
    body['organization'] = new_org.as_dict()
    # Insert Org Address
    new_org_addr = insert_address(data=data, new_org_id=new_org_id, dt_now=dt_now, org=True, add=True, flush=False)
    current_app.logger.info('Inserted record:\n',new_org_addr)
    body['org_address'] = new_org_addr.as_dict()
    # Insert Location Address (Ship to)
    new_loc_addr = insert_address(data=data, new_org_id=new_org_id, dt_now=dt_now, org=False, add=True, flush=True)
    current_app.logger.info('Inserted record:\n',new_loc_addr)
    body['loc_address'] = new_loc_addr.as_dict()
    new_loc_addr_id = new_loc_addr.id # Fetching address id of new record
    # Insert Account
    new_accnt = insert_account(data=data, new_org_id=new_org_id, new_loc_addr_id=new_loc_addr_id, dt_now=dt_now, add=True, flush=True)
    current_app.logger.info('Inserted record:\n',new_accnt)
    body['loc_address'] = new_loc_addr.as_dict()
    new_accnt_id = new_accnt.id
    # Insert Person
    new_person = insert_person(data=data, new_org_id=new_org_id, dt_now=dt_now, add=True, flush=True)
    current_app.logger.info('Inserted record:\n',new_person)
    body['person'] = new_person.as_dict()
    new_person_id = new_person.id
    # Insert PersonAccount
    new_person_accnt = insert_person_account(data=data, new_accnt_id=new_accnt_id, new_person_id=new_person_id, dt_now=dt_now, add=True, flush=False)
    current_app.logger.info('Inserted record:\n',new_person_accnt)
    body['person_account'] = new_person_accnt.as_dict()
    # Insert Restaurant
    new_restaurant = insert_restaurant(data=data, new_org_id=new_org_id, dt_now=dt_now, add=True, flush=False)
    current_app.logger.info('Inserted record:\n',new_restaurant)
    body['restaurant'] = new_restaurant.as_dict()

    db.session.commit()
    body['success']=True
    db.session.close()
    return json.dumps(body, default=converter), 200

def insert_account(data, new_org_id, new_loc_addr_id, dt_now, add=True, flush=True):
    """
    Utility function to insert new account 

    data: POST request json body
    new_org_id: associated organization id
    new_loc_addr_id: associated address for this account
    dt_now: pre-calculated datetime object
    add: whether db.session will add
    flush: whether db.session will flush
    """
    new_accnt = Account(
        organization_id=new_org_id,
        address_id=new_loc_addr_id,
        account_number=uuid.uuid1().hex,
        account_name=data['account_name'],
        created_at=dt_now,
        timezone_name='Pacific Daylight Time/Vancouver' # Default value for now. Manually hard-coded because MySQL  table doesn't have default for this
    )
    if add==True:
        db.session.add(new_accnt)
    if flush == True:
        db.session.flush()

    return new_accnt