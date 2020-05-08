import os
import traceback
import logging
from flask import jsonify, request, abort, make_response, render_template, current_app, session
from . import api
from web.api.api_utils import get_supplier_obj, concatenate_order_responses
from web.preprocessor.trp_test import run, ProcessedDocument
from web.preprocessor.trp import Document
from web.connections.s3_connection import S3Interface
from web.connections.DBConnection import DBConn
from web.constants import S3_BUCKET_NAME, S3_IMAGE_BUCKET_NAME, S3_PREPROCESSED_INVOICES_BUCKET
<<<<<<< HEAD
from web.models.account import Account
from web.models.country import Country
from web.database import db, Base
from datetime import datetime as dt
import web.auth as auth
from web.auth import requires_auth
=======
from web.database import db
>>>>>>> 2fa941ac476ff8a95e074f89941c76cef8f1cf20

logger = logging.getLogger(__name__)

# signal definition
def log_request(sender, **extra):
    if request.method == 'POST':
        message = 'Not able to make a POST request'
    elif request.method == 'GET':
        message = 'Not able to find bucket'
    sender.logger.info(message)

# custom 404 error handler
@api.app_errorhandler(404)
def page_not_found(e):
    current_app.logger.warn(f'404 not found: {request.path}')
    current_app.logger.warn(e)
    return 'API not Found', 404

# custom 500 error handler
@api.app_errorhandler(500)
def server_error(e):
    current_app.logger.warn('500 internal server error')
    current_app.logger.warn(e)
    return '500 Internal Server Error', 500


@api.route('/')
@requires_auth
def hello_whale():
    return render_template("whale_hello.html")

@api.route('/preprocess', methods=['GET'])
def preprocess():
    try:
        print(request.args)
        print(request.view_args)
        print(run())
        return make_response(jsonify({'hello': 'world'}))
    except Exception as exc:
        traceback.print_exc()
        return abort(400)

@api.route('/connection', methods=['GET'])
def connection():
    try:
        obj = DBConn()
        result = obj.get_query('show databases;', True)

        return make_response(jsonify({'query_result': result}))
    except Exception as exc:
        traceback.print_exc()
        return make_response(jsonify({'Error': exc}))


# TO DO: Move this to api_utils when finished
def parse_file_name(textract_file_name):
    """
    Given Textract json response filename, return the s3 key (including the bucket) for the corresponding image, the account number, and the supplier_id
    """
    # Image file name is same as Textract filename with ".json appended to the end"
    image_file_name = textract_file_name[:-5]
    # S3 image key will be sent to the DataBase with each lineitem, so bucket name and filename is used
    s3_image_key = S3_IMAGE_BUCKET_NAME+'/'+image_file_name
    # Account number will always be the first portion of the file name, separated by "/"
    account_number = textract_file_name.split('/')[0]
    # Supplier Id will be at the end of the file, separated by "-"
    organization_number = image_file_name.split('-')[-1]
    # TO DO: Remove below lines. These were placed here before organization number was appended to the end of the file
    organization_number = 'd7a8755d85ce11eab51c0aedbe94' # <- temp: sysco org number 
    # organization_number = '2c9fb715f5c21ec8f8618efd31b7' # <- temp: freshpoint org number 
    account_number = 'debddd37-82a9-11ea-b51c-0aedbe94' # <- temp: account number
    return s3_image_key, account_number, organization_number

@api.route('/s3-connect', methods=['GET'])
def s3_connect():
    try:
        file_name = request.args.get('file_name')
        s3_image_key, account_number, supplier_organization_number = parse_file_name(textract_file_name=file_name)
        # Fetch template
        template_name = get_supplier_obj(supplier_organization_number).template_name
        # Fetch Textract response
        s3_obj = S3Interface(S3_BUCKET_NAME)
        resp = s3_obj.get_file(file_name)
        doc = Document(resp)
        
        processed_doc = ProcessedDocument(doc=doc,
                                        s3_image_key=s3_image_key, 
                                        supplier_org_num= supplier_organization_number,
                                        account_number=account_number,
                                        template_name=template_name)
        processed_doc.processDocument()
        return concatenate_order_responses(processed_doc._order_tsv,processed_doc._orderitem_tsv), 200
    except Exception as exc:
        traceback.print_exc()
        return abort(400)

@api.route('/s3-upload', methods=['POST'])
def upload_invoice():
    error = False
    try:
        file_name = request.get_json()['file_name']
        s3_image_key, account_number, supplier_organization_number = parse_file_name(textract_file_name=file_name)
        # Fetch template
        template_name = get_supplier_obj(supplier_organization_number).template_name
        # Fetch Textract response
        s3_obj = S3Interface(S3_BUCKET_NAME)
        resp = s3_obj.get_file(file_name)
        doc = Document(resp)
        
        processed_doc = ProcessedDocument(doc=doc,
                                        s3_image_key=s3_image_key, 
                                        supplier_org_num= supplier_organization_number,
                                        account_number=account_number,
                                        template_name=template_name)
        processed_doc.processDocument()
        # Pulling buffers and account number for upload
        order_tsv_buf = processed_doc._order_buf
        orderitems_tsv_buf = processed_doc._orderitem_buf
        accnt_no = processed_doc._account_number
        invoice_num = processed_doc.invoice_number
        # Uploading header
        s3_obj.upload_file(order_tsv_buf, S3_PREPROCESSED_INVOICES_BUCKET, accnt_no,filetype='header', invoice_number=invoice_num)
        # Uploading orderitems
        s3_obj.upload_file(orderitems_tsv_buf, S3_PREPROCESSED_INVOICES_BUCKET, accnt_no,filetype='lineitem', invoice_number=invoice_num)
    except:
        error = True
        traceback.print_exc()
        return abort(500) 
    
    return concatenate_order_responses(processed_doc._order_tsv,processed_doc._orderitem_tsv), 200

@api.route('/login')
def login():
    # import pdb;pdb.set_trace()
    return auth.auth0.authorize_redirect(redirect_uri='http://localhost:5000/api/callback')


@api.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth.auth0.authorize_access_token()
    resp = auth.auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return make_response('yes', 200)
