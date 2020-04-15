import os
import traceback
from flask import jsonify, request, abort, make_response, render_template
from . import api
from web.preprocessor.trp_test import run, processDocument
from web.preprocessor.trp import Document
from web.connections.s3_connection import S3Interface
from web.connections.DBConnection import DBConn
from web.constants import S3_BUCKET_NAME


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
        return make_response(jsonify({'query_result': result}))
    except Exception as exc:
        traceback.print_exc()
        return make_response(jsonify({'host': obj.host}))


@api.route('/s3-connect', methods=['GET'])
def s3_connect():
    try:
        file_name = request.args.get('file_name')
        s3_obj = S3Interface(S3_BUCKET_NAME)
        resp = s3_obj.get_file(file_name)
        doc = Document(resp)
        resp = processDocument(doc)
        return make_response(resp)
    except Exception as exc:
        traceback.print_exc()
        return abort(400)
