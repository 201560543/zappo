from datetime import datetime, date
from functools import wraps
from flask import current_app, abort, make_response
from web.database import db
from web.models.organization import Organization
from web.models.supplier import Supplier

def converter(obj):
    """
    Used to convert an object into a json-serializable representation for api calls
    """
    if isinstance(obj, datetime):
        return obj.__str__()
    elif isinstance(obj, date):
        return obj.__str__()


def exception_handler(**kw):
    """
    Function to handle all code errors and logs for us. This function also takes
    keyword arguments. If you want to add more arguments here then make sure to check for
    them as show below:
    Arguments:
    kw: (keyword argumets) {
        'custom_msg': ''
    }
    """
    custom_msg = kw.get('custom_msg', 'Found an exception while making a request')
    def handler(func):
        """
        Main function wrapper
        """
        @wraps(func)
        def inner(*args, **kwargs):
            """
            Inner function to log all issues
            """
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                current_app.logger.warn(custom_msg)
                current_app.logger.warn(exc)
                abort(400, description='Kindly contact your dev team to handle this error')
        return inner
    return handler

def concatenate_order_responses(order_tsv, orderitem_tsv):
    """
    For api response, concatenate both order header and orderitem TSVs for the response
    """
    pre_head = "\n=====ORDER HEADER=====\n"
    pre_item = "\n\n=====ORDERITEMS=====\n"
    no_items = "\n\n=====NO ITEMS=====\n"
    if orderitem_tsv == None:
        raw_resp = pre_head + order_tsv + no_items
    else:
        raw_resp = pre_head + order_tsv + pre_item + orderitem_tsv

    return make_response(raw_resp)

def get_supplier_obj(supplier_organization_number):
    """
    Given a supplier organization number, fetch the supplier
    """
    org = db.session.query(Organization).filter_by(organization_number=supplier_organization_number).one_or_none()
    if org == None:
        current_app.logger.warn(f'404 supplier with organization number {supplier_organization_number} not found.')
        raise Exception
    supplier = db.session.query(Supplier).filter_by(organization_id=org.id).one_or_none()
    if supplier == None:
        current_app.logger.warn(f'404 supplier with organization ID {org.id} not found.')
        raise Exception
    return supplier