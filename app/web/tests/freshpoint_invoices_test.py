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

class FreshTest1(CommonTests, unittest.TestCase):
    def setUp(self):
        self.app = create_app(base)
        self.response = file_load("../data/freshpoint/20200424_090016.jpg.json")
        self.doc = Document(self.response)
        
    def test_orders(self):
        self.order = self.compute_order(self.doc.pages[0])
        self.assertEqual(self.order.invoice_number, '1478455')
        self.assertEqual(self.order.invoice_date, '2017-10-28')
        self.assertEqual(self.order.customer_account_number, '605211')
    
    def test_order_items(self):
        with self.app.app_context():
            self.processed_doc = ProcessedDocument(self.doc, '', '', '', 'freshpoint.json')
            self.processed_doc.processDocument()
            df = self.processed_doc._orderitem_obj._TableDataFrame
            # textract doesn't read the first row well
            # For second row
            self.assertEqual(df.iloc[1]['item_number'], '238050')
            self.assertEqual(df.iloc[1]['size'], '24')
            self.assertEqual(df.iloc[1]['weight'], '14.00')
            self.assertEqual(df.iloc[1]['price'], '25.20')

