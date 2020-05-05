import requests
from datetime import datetime as dt
from flask import Flask
from flask_testing import LiveServerTestCase
from web import create_app
from web.config import base
from web.database import db
from web.models.account import Account

class MyTest(LiveServerTestCase):

    def create_app(self):
        app = create_app(base)
        app.config['TESTING'] = True
        # Default port is 5000
        app.config['LIVESERVER_PORT'] = 8943
        # Default timeout is 5 seconds
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app

    def test_server_is_up_and_running(self):
        response = requests.get(f'{self.get_server_url()}/api')
        self.assertEqual(response.status_code, 200)
    
    # def test_account_api_save(self):
    #     try:
    #         new_accnt = Account(
    #                 organization_id=1,
    #                 # address_id=2,
    #                 account_number='3',
    #                 account_name='4',
    #                 created_at=dt.now(),
    #                 timezone_name='tz_name' 
    #             )

    #         db.session.add(new_accnt)
    #         db.session.commit()
    #     except Exception as exc:
    #         print(exc)
    #     res = db.session.query(Account).all()
    #     self.assertEqual(len(res), 1)

    
    # def test_account_api(self):
    #     res = db.session.query(Account).all()
    #     self.assertEqual(res, True)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()