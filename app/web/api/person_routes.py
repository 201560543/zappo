import json
from . import person
from web.models.person import Person
from web.api.api_utils import converter, exception_handler
from web.database import db
from flask import current_app, request

@person.route('/', methods=['GET'])
@exception_handler(custom_msg="Issues in fetching all suppliers")
def get_all_people(return_json=True):
    results = db.session.query(Person).all()
    result_dict = [result.as_dict() for result in results]# if result.is_deleted==0] # No is_deleted for person
    current_app.logger.info(result_dict)
    if return_json==True:
        return json.dumps(result_dict, default=converter)
    else:
        return result_dict


def insert_person(data, org_id, dt_now, add=True, flush=True):
    """
    Utility function to insert new person 

    data: POST request json body
    org_id: associated organization id
    dt_now: pre-calculated datetime object
    add: whether db.session will add
    flush: whether db.session will flush
    """
    new_person = Person(
        organization_id=org_id,
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        username='temp', # Todo: remove this column. No user data stored in this DB, only Auth0
        password='temp', # Todo: remove this column. No user data stored in this DB, only Auth0
        created_at=dt_now
        # ,auth0_id= # TO DO: Add this column to the database before enabling this as a parameter
    )
    if add==True:
        db.session.add(new_person)
    if flush == True:
        db.session.flush()

    return new_person