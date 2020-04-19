import traceback
import logging
from flask import Flask, render_template, jsonify, request, abort, make_response, current_app
from preprocessor.trp_test import run, processDocument
from preprocessor.trp import Document
from connections.s3_connection import S3Interface
from connections.DBConnection import DBConn
from constants import S3_BUCKET_NAME


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


@app.route('/')
def hello_whale():
    return render_template("whale_hello.html")

@app.route('/preprocess', methods=['GET'])
def preprocess():
    try:
        print(request.args)
        print(request.view_args)
        print(run())
        return make_response(jsonify({'hello': 'world'}))
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
        s3_obj = S3Interface(S3_BUCKET_NAME)
        resp = s3_obj.get_file(file_name)
        doc = Document(resp)
        resp = processDocument(doc)
        return make_response(resp)
    except Exception as exc:
        traceback.print_exc()
        return abort(400)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
