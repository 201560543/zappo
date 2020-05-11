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


def insert_address(data, new_org_id, dt_now, org=True, add=True, flush=True):
    """
    Utility function to insert new address 

    data: POST request json body
    new_org_id: associated organization id
    dt_now: pre-calculated datetime object
    org: Whether input data is an organization address or location address. Parameters will differ based on this choice
    add: whether db.session will add
    flush: whether db.session will flush
    """
    if org==True:
        new_addr = Address(
            organization_id=new_org_id,
            address_type_id=1, # 1 (sold to) is the default organization address type
            country_id=data['org_country_id'],
            address_name=data['org_street_address'],
            postal_code=data['org_postal_code'],
            # province_state=data['org_provice_state'], # TO DO: Add this column to the database before enabling this as a parameter
            city_name=data['org_city'],
            from_date=dt_now.date(),
            created_at=dt_now
        )
    else: 
        new_addr = Address(
            organization_id=new_org_id,
            address_type_id=2, # 1 (ship to) is the default organization address type
            country_id=data['loc_country_id'],
            address_name=data['loc_street_address'],
            postal_code=data['loc_postal_code'],
            # province_state=data['loc_provice_state'], # TO DO: Add this column to the database before enabling this as a parameter
            city_name=data['loc_city'],
            from_date=dt_now,
            created_at=dt_now
        )
    if add==True:
        db.session.add(new_addr)
    if flush == True:
        db.session.flush()

    return new_addr