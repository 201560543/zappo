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

class Cioffis1(CommonTests, unittest.TestCase):
    def setUp(self):
        self.app = create_app(base)
        self.response = file_load("../data/cioffis/20191103_193208.jpg.json")
        self.doc = Document(self.response)
        
    def test_orders(self):
        self.order = self.compute_order(self.doc.pages[0], template_name='cioffi.json')
        self.assertEqual(self.order.invoice_number, '932312')
        self.assertEqual(self.order.invoice_date, '2018-02-02')
        self.assertEqual(self.order.customer_account_number, '1561')
    
    def test_orders_incorrect_template(self):
        with self.assertRaises(Exception):
            self.compute_order(self.doc.pages[0], template_name='freshpoint.json')
    
    def test_order_items(self):
        with self.app.app_context():
            self.processed_doc = ProcessedDocument(self.doc, '', '', '', 'cioffi.json')
            self.processed_doc.processDocument()
            df = self.processed_doc._orderitem_obj._TableDataFrame
            # textract doesn't read the first row well
            # For second row
            self.assertEqual(df.iloc[0]['item_number'], 's00951')
            self.assertEqual(df.iloc[0]['shipped_quantity'], '19.18')
            self.assertEqual(df.iloc[0]['price'], '10.99')
            self.assertEqual(df.iloc[0]['total_price'], '210.79')

