import os
import traceback
import logging
from flask import jsonify, request, abort, make_response, render_template, current_app
from . import api
from web.preprocessor.trp_test import run, ProcessedDocument
from web.preprocessor.trp import Document
from web.connections.s3_connection import S3Interface
from web.connections.DBConnection import DBConn
from web.constants import S3_BUCKET_NAME, S3_IMAGE_BUCKET_NAME, S3_PREPROCESSED_INVOICES_BUCKET
# from web.models.account import Account
from web.database import db, prepare_automap_base, create_autogen_table

logger = logging.getLogger(__name__)

# signal definition
def log_request(sender, **extra):
    if request.method == 'POST':
        message = 'Not able to make a POST request'
    elif request.method == 'GET':
        message = 'Not able to find bucket'
    sender.logger.info(message)

# custom 404 error handler
@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'detail': 'Not found'}), 404)


# custom 400 error handler
@api.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'detail': 'Bad request'}), 400)


@api.route('/')
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
        Base = prepare_automap_base(db)
        Account = Base.classes.account

        # Using automap object
        for account in db.session.query(Account).all():
            print(account.account_number)
        
        # Using autoloaded table
        Supplier = create_autogen_table(db,'supplier')
        print(db.session.query(Supplier).all())
        
        return make_response(jsonify({'query_result': result}))
    except Exception as exc:
        traceback.print_exc()
        return make_response(jsonify({'host': obj.host}))

# TO DO: Add functionality to parse the account number and supplier id from the file name
# TO DO: Make sure line items are uploaded to S3 with file name
# TO DO: Replace supplier with supplier_id
def parse_file_name(textract_file_name, S3_IMAGE_BUCKET_NAME):
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
    supplier_id = image_file_name.split('-')[-1]
    return s3_image_key, account_number, supplier_id

@api.route('/s3-connect', methods=['GET'])
def s3_connect():
    try:
        file_name = request.args.get('file_name')
        template_name = request.args.get('template_name')+'.json' # TO DO: Deprecate this parameter when we have query functionality on supplier table and supplier_id can be parsed from file_name
        
        # # TO DO: Implement this after implementing GET api on supplier information
        s3_image_key, _, _ = parse_file_name(textract_file_name=file_name, S3_IMAGE_BUCKET_NAME=S3_IMAGE_BUCKET_NAME)
        s3_obj = S3Interface(S3_BUCKET_NAME)
        resp = s3_obj.get_file(file_name)
        doc = Document(resp)
        processed_doc = ProcessedDocument(doc)
        processed_doc.set_s3_image_key(s3_image_key)
        processed_doc.processDocument(template_name=template_name)
        return make_response(processed_doc._orderitem_tsv)
    except Exception as exc:
        traceback.print_exc()
        return abort(400)

@api.route('/s3-upload', methods=['POST'])
def upload_invoice():
    error = False
    try:
        file_name = request.get_json()['file_name']
        template_name = request.get_json()['template_name']+'.json'
        # # TO DO: Implement this after implementing GET api on supplier information
        s3_image_key, _, _ = parse_file_name(textract_file_name=file_name, S3_IMAGE_BUCKET_NAME=S3_IMAGE_BUCKET_NAME)
        s3_obj = S3Interface(S3_BUCKET_NAME)
        resp = s3_obj.get_file(file_name)
        doc = Document(resp)
        processed_doc = ProcessedDocument(doc)
        # Setting image key
        processed_doc.set_s3_image_key(s3_image_key)
        # Processing Document
        processed_doc.processDocument(template_name=template_name)
        # Pulling buffers and account number for upload
        order_tsv_buf = processed_doc._order_buf
        orderitems_tsv_buf = processed_doc._orderitem_buf
        orderitems_tsv_raw = processed_doc._orderitem_tsv
        accnt_no = processed_doc._account_number
        # Uploading header
        s3_obj.upload_file(order_tsv_buf, S3_PREPROCESSED_INVOICES_BUCKET, accnt_no,type='header')
        # Uploading orderitems
        s3_obj.upload_file(orderitems_tsv_buf, S3_PREPROCESSED_INVOICES_BUCKET, accnt_no,type='lineitem')
    except:
        error = True
        traceback.print_exc()
        return abort(500) 
    
    return make_response(orderitems_tsv_raw), 200