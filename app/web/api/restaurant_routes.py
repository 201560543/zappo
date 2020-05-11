import json
from . import restaurant
from web.models.restaurant import Restaurant
from web.api.api_utils import converter, exception_handler
from web.database import db
from flask import current_app, request

@restaurant.route('/', methods=['GET'])
@exception_handler(custom_msg="Issues in fetching all suppliers")
def get_all_restaurants(return_json=True):
    results = db.session.query(Restaurant).all()
    result_dict = [result.as_dict() for result in results if result.is_deleted==0]
    current_app.logger.info(result_dict)
    if return_json==True:
        return json.dumps(result_dict, default=converter)
    else:
        return result_dict


def insert_restaurant(data, new_org_id, dt_now, add=True, flush=True):
    """
    Utility function to insert new person_account 

    data: POST request json body
    new_org_id: associated organization id
    dt_now: pre-calculated datetime object
    add: whether db.session will add
    flush: whether db.session will flush
    """
    new_restaurant = Restaurant(
        organization_id=new_org_id,
        restaurant_name=data['account_name'],
        created_at=dt_now
    )
    if add==True:
        db.session.add(new_restaurant)
    if flush == True:
        db.session.flush()

    return new_restaurant