import os
import traceback
import logging
from flask import jsonify, request, abort, make_response, render_template, current_app
from . import api
from web.preprocessor.trp_test import run, ProcessedDocument
from web.preprocessor.trp import Document
from web.connections.s3_connection import S3Interface
from web.connections.DBConnection import DBConn
from web.constants import S3_BUCKET_NAME
from web.models.account import Account
from web.models.country import Country
from web.database import db, Base
from datetime import datetime as dt

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
        # country = Base.classes.Country
        # print(db.session.query(country).all())

        countries = db.session.query(Country).all()
        print([c.__dict__ for c in countries])

        return make_response(jsonify({'query_result': result}))
    except Exception as exc:
        traceback.print_exc()
        return make_response(jsonify({'Error': exc}))


@api.route('/s3-connect', methods=['GET'])
def s3_connect():
    try:
        file_name = request.args.get('file_name')
        template_name = request.args.get('template_name')+'.json' # TO DO: need to discuss whether we will detect template or take template as a parameter
        s3_obj = S3Interface(S3_BUCKET_NAME)
        resp = s3_obj.get_file(file_name)
        doc = Document(resp)
        processed_doc = ProcessedDocument(doc)
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
        template_name = request.get_json()['template_name']
        s3_obj = S3Interface(S3_BUCKET_NAME)
        resp = s3_obj.get_file(file_name)
        doc = Document(resp)
        processed_doc = ProcessedDocument(doc)
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