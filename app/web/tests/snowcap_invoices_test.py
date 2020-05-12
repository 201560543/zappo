import json
import unittest
from web.preprocessor.trp import Document 
from web.preprocessor.trp_test import ProcessedDocument
from web.models.orders import Order
from .constants import TEST_DIR, TEST_ACCNT_NUM, TEST_ORG_NUM
from web import create_app
from web.config import base
import csv
from .utils import CommonTests, file_load

import os
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class SnowcapTest1(CommonTests, unittest.TestCase):
    def setUp(self):
        self.app = create_app(base)
        self.response = file_load("../data/snowcap/20190326_122931.json")
        self.doc = Document(self.response)
        
    def test_orders(self):
        self.order = self.compute_order(self.doc.pages[0], template_name="snowcap.json")
        self.assertEqual(self.order.invoice_number, 'NO.')
        self.assertEqual(self.order.customer_account_number, '17110')
    
    def test_order_items(self):
        with self.app.app_context():
            self.processed_doc = ProcessedDocument(self.doc, '', '', '', 'snowcap.json')
            self.processed_doc.processDocument()
            df = self.processed_doc._orderitem_obj._TableDataFrame
            print(df)
            self.check_order_items_row(
                df.iloc[0],
                {'item_number': 'av2123', 'shipped_quantity': '1', 'size': '6/687g',
                'price': '24.09', 'total_price': '24.09'}
            )
            self.check_order_items_row(
                df.iloc[1],
                {'item_number': 'av201i', 'shipped_quantity': '1',
                'price': '20.40', 'total_price': '20'}
            )
            self.check_order_items_row(
                df.iloc[2],
                {'item_number': 'gz362', 'shipped_quantity': '1', 'size': '6/6226',
                'price': '36.66', 'total_price': '36.66'}
            )