import json
import unittest
from web.preprocessor.trp import Document 
from web.preprocessor.trp_test import ProcessedDocument
from web.models.orders import Order
from web.tests.constants import TEST_DIR, TEST_ACCNT_NUM, TEST_ORG_NUM
from web import create_app
from web.config import base
import csv

import os
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def file_load(file_name):
    with open(file_name, 'r') as document:
        return json.loads(document.read())

class FreshpointCommonTests(object):
    def test_document_upload(self):
        self.assertTrue(self.response is not None)
        self.assertTrue(self.doc is not None)

    def test_document_pages(self):
        self.assertEqual(len(self.doc.pages), 1)

    def test_document_tables(self):
        first_page = self.doc.pages[0]
        self.assertEqual(len(first_page.tables) != 0, True)

    def compute_order(self, first_page):
        order = Order(supplier_organization_number=TEST_ORG_NUM, 
                        account_number=TEST_ACCNT_NUM)
        order.set_order_values(first_page, 'freshpoint.json')
        return order

class FreshTest1(FreshpointCommonTests, unittest.TestCase):
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
            self.assertEqual(df.iloc[1]['size'], '24 CT')
            self.assertEqual(df.iloc[1]['weight'], '14.00')
            self.assertEqual(df.iloc[1]['price'], '25.20')

    



