import json
from . import address_type
from web.models.address_type import AddressType
from web.api.api_utils import converter, exception_handler
from web.database import db
from flask import current_app, request

@address_type.route('/', methods=['GET'])
@exception_handler(custom_msg="Issues in fetching all address types")
def get_all_addr_types(return_json=True):
    results = db.session.query(AddressType).all()
    result_dict = [result.as_dict() for result in results]
    current_app.logger.info(result_dict)
    if return_json==True:
        return json.dumps(result_dict, default=converter)
    else:
        return result_dict