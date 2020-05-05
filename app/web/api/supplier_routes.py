import json
from . import supplier
from web.models.supplier import Supplier
from web.api.api_utils import converter, exception_handler
from web.database import db
from flask import current_app, request

@supplier.route('/', methods=['GET'])
@exception_handler(custom_msg="Issues in fetching all suppliers")
def get_all_suppliers(return_json=True):
    results = db.session.query(Supplier).all()
    result_dict = [result.as_dict() for result in results if result.is_deleted==0]
    current_app.logger.info(result_dict)
    if return_json==True:
        return json.dumps(result_dict, default=converter)
    else:
        return result_dict