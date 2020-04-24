import traceback
from flask import Flask, render_template, jsonify, request, abort, make_response, current_app
import logging
from preprocessor.trp_test import run, ProcessedDocument
from preprocessor.trp import Document
from connections.s3_connection import S3Interface
from connections.DBConnection import DBConn
from constants import S3_BUCKET_NAME, S3_PREPROCESSED_INVOICES_BUCKET


app = Flask(__name__)
logger = logging.getLogger(__name__)

# signal definition
def log_request(sender, **extra):
    if request.method == 'POST':
        message = 'Not able to make a POST request'
    elif request.method == 'GET':
        message = 'Not able to find bucket'
    sender.logger.info(message)

# custom 404 error handler
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'detail': 'Not found'}), 404)


# custom 400 error handler
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'detail': 'Bad request'}), 400)

# custom 500 error handler
@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'detail': 'Internal Server Error'}), 500)

@app.route('/')
def hello_whale():
    return render_template("whale_hello.html")

@app.route('/preprocess', methods=['GET'])
def preprocess():
    try:
        # print(request.args)
        # print(request.view_args)
        orderitem_tsv = run()

        return make_response(orderitem_tsv)
    except Exception as exc:
        traceback.print_exc()
        return abort(400)

@app.route('/connection', methods=['GET'])
def connection():
    try:
        current_app.logger.info('Testing logging capabalities for db connection')
        obj = DBConn()
        result = obj.get_query('show databases;', True)
        return make_response(jsonify({'query_result': result}))
    except Exception as exc:
        traceback.print_exc()
        return make_response(jsonify({'host': obj.host}))

@app.route('/s3-connect', methods=['GET'])
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

@app.route('/s3-upload', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
