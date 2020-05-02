import json
from . import supplier
from web.models.supplier import Supplier
from web.api.api_utils import converter, exception_handler
from web.database import db
from flask import current_app, request

@supplier.app_errorhandler(404)
def page_not_found(e):
    current_app.logger.warn(f'404 not found')
    current_app.logger.warn(e)
    return 'Supplier API not Found', 404

@supplier.app_errorhandler(500)
def server_error(e):
    current_app.logger.warn('500 internal server error')
    current_app.logger.warn(e)
    return '500 Internal Server Error', 500

@supplier.route('/', methods=['GET'])
@exception_handler(custom_msg="Issues in fetching all suppliers")
def get_all_suppliers(return_json=True):
    results = db.session.query(Supplier).all()
    result_dict = [result.as_dict() for result in results]
    current_app.logger.info(result_dict)
    if return_json==True:
        return json.dumps(result_dict, default=converter)
    else:
        return result_dict