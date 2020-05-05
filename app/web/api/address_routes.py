from . import address
from web.models.address import Address
from web.api.api_utils import converter, exception_handler
from datetime import date as d
from datetime import datetime as dt
from web.database import db
import json
from flask import jsonify, request, current_app, abort

@address.route('/', methods=['GET'])
@exception_handler(custom_msg='Issue in fetching all addresses')
def get_all_adresses(return_json=True):
    # TO DO: Add error handling
    results = db.session.query(Address).all()
    result_dicts = [adr.as_dict() for adr in results if adr.is_deleted==0] # Condition to not reveal soft-deleted address to client
    current_app.logger.info(result_dicts)
    if return_json == True:
        return json.dumps(result_dicts, default=converter)
    else:
        return result_dicts

@address.route('/create', methods=['POST'])
@exception_handler(custom_msg='Issue in POSTing new address')
def create_address():
    # TODO: Add error handling
    body = {}
    # Fetching values
    # addr_name = request.get_json()['name'] # TODO ask Franck to add a name to address table. see https://dev.zappotrack.com/#/settings/locations
    addr_address = request.get_json()['address']
    addr_address_type_id = request.get_json()['address_type_id'] # TODO: figure out how to properly set address type. May need to set front end param
    addr_city = request.get_json()['city']
    # addr_province = request.get_json()['province'] # TODO ask Franck or Riti if Province is required
    addr_postal_code = request.get_json()['postal_code']
    addr_organization_id = request.get_json()['organization_id']
    addr_country_id = request.get_json()['country_id'] # TODO: set country route so Subodh can get country ID from user-given country

    # Creating new address
    new_address = Address(
        organization_id=addr_organization_id,
        address_type_id=addr_address_type_id,
        country_id=addr_country_id,
        address_name=addr_address,
        postal_code=addr_postal_code,
        city_name=addr_city,
        from_date=d.fromisoformat('9999-01-01'),
        created_at=dt.now()
    )
    body['obj']=new_address.as_dict()

    db.session.add(new_address)
    db.session.commit()
    current_app.logger.info('Inserted record:\n',new_address)
    db.session.close()
    body['success']=True
    return jsonify(body)

@address.route('/delete/<int:address_id>', methods=['DELETE'])
@exception_handler(custom_msg='Issue in soft DELETE-ing address')
def soft_delete_address(address_id):
    result = db.session.query(Address).filter_by(id=address_id).one_or_none()
    if result == None:
        abort(404)
    current_app.logger.info(f"Record to be soft deleted: Address.id={address_id}")
    # Set delete flag
    result.is_deleted=1
    # Commit changes
    db.session.commit()
    body = {
        "success": True,
        "message": "Record set to deleted",
        "record": result.as_dict()
    }
    return jsonify(body), 202

