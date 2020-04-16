from flask import g
from web import create_app, db
from web.config import base
from web.database import db_session

app = create_app(base)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
