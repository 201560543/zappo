import json
from . import person_account
from web.models.person_account import PersonAccount
from web.api.api_utils import converter, exception_handler
from web.database import db
from flask import current_app, request

@person_account.route('/', methods=['GET'])
@exception_handler(custom_msg="Issues in fetching all suppliers")
def get_all_person_accounts(return_json=True):
    results = db.session.query(PersonAccount).all()
    result_dict = [result.as_dict() for result in results]# if result.is_deleted==0] # No is_deleted for person_account
    current_app.logger.info(result_dict)
    if return_json==True:
        return json.dumps(result_dict, default=converter)
    else:
        return result_dict

def insert_person_account(data, accnt_id, person_id, dt_now, add=True, flush=True):
    """
    Utility function to insert new person_account 

    data: POST request json body
    accnt_id: associated account id
    person_id: associated person id
    dt_now: pre-calculated datetime object
    add: whether db.session will add
    flush: whether db.session will flush
    """
    new_person_accnt = PersonAccount(
        account_id=accnt_id,
        person_id=person_id,
        is_admin=data['is_admin'], 
        role_name=data['role_name'], 
        from_date=dt_now,
        created_at=dt_now
    )
    if add==True:
        db.session.add(new_person_accnt)
    if flush == True:
        db.session.flush()

    return new_person_accnt