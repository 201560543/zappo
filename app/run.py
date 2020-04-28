from web import create_app, db
from web.config import base

app = create_app(base)

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True, host='0.0.0.0')

