from web import create_app, db
from web.config import base
# from web.database import db_session

app = create_app(base)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

