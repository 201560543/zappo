import json
from . import organization
from web.models.organization import Organization
from web.api.api_utils import converter, exception_handler
from web.database import db
from flask import current_app, request

@organization.app_errorhandler(404)
def page_not_found(e):
    current_app.logger.warn(f'404 not found')
    current_app.logger.warn(e)
    return 'Organization API not Found', 404

@organization.app_errorhandler(500)
def server_error(e):
    current_app.logger.warn('500 internal server error')
    current_app.logger.warn(e)
    return '500 Internal Server Error', 500

@organization.route('/', methods=['GET'])
@exception_handler(custom_msg='Issues in fetching all organizations')
def get_all_suppliers(return_json=True):
    results = db.session.query(Organization).all()
    # Return only suppliers (organization_type_id==3)
    result_dicts = [acnt.as_dict() for acnt in results if acnt.organization_type_id==3]
    current_app.logger.info(result_dicts)
    if return_json == True:
        return json.dumps(result_dicts, default=converter)
    else:
        return result_dicts

@organization.route('/<org_number>', methods=['GET'])
@exception_handler(custom_msg='Issues in fetching org by org number')
def get_organization_by_org_number(org_number, return_json=True):
    result = db.session.query(Organization).filter_by(organization_number=org_number).one_or_none()
    result_dict = result.as_dict()
    current_app.logger.info(result_dict)
    if return_json == True:
        return json.dumps(result_dict, default=converter)
    else:
        return result_dict