import json
from . import organization
from sqlalchemy import and_
from web.models.organization import Organization
from web.api.api_utils import converter, exception_handler
from web.database import db
from flask import current_app, request, abort

@organization.route('/', methods=['GET'])
@exception_handler(custom_msg='Issues in fetching all organizations')
def get_all_organizations(return_json=True):
    results = db.session.query(Organization).filter_by(is_deleted=0)
    result_dicts = [acnt.as_dict() for acnt in results if acnt.organization_type_id]
    current_app.logger.info(result_dicts)
    if return_json == True:
        return json.dumps(result_dicts, default=converter)
    else:
        return result_dicts

@organization.route('/<org_number>', methods=['GET'])
@exception_handler(custom_msg='Issues in fetching org by org number')
def get_organization_by_org_number(org_number, return_json=True):
    result = db.session.query(Organization)\
            .filter(and_(
                Organization.organization_number==org_number,
                Organization.is_deleted==0
                )
            ).one_or_none()

    # If we don't have any result then we should send a 400 error
    if result is None:
        abort(400, description="Organization ID doesn't exist")

    result_dict = result.as_dict()
    current_app.logger.info(result_dict)
    if return_json == True:
        return json.dumps(result_dict, default=converter)
    else:
        return result_dict