import traceback
from flask import Flask, render_template, jsonify, request, abort, make_response

app = Flask(__name__)

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

        return make_response(jsonify({'hello': 'world'}))
    except Exception as exc:
        print(e)
        traceback.print_exc()
        return abort(400)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
