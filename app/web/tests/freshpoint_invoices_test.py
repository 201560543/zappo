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

class FreshTest2(CommonTests, unittest.TestCase):
    def setUp(self):
        self.app = create_app(base)
        self.response = file_load("../data/freshpoint/20200424_085933.jpg.json")
        self.doc = Document(self.response)
        
    def test_orders(self):
        self.order = self.compute_order(self.doc.pages[0])
        self.assertEqual(self.order.invoice_number, '1496695')
        self.assertEqual(self.order.invoice_date, '2018-03-23')
        self.assertEqual(self.order.customer_account_number, '605211')
    
    def test_order_items(self):
        with self.app.app_context():
            self.processed_doc = ProcessedDocument(self.doc, '', '', '', 'freshpoint.json')
            self.processed_doc.processDocument()
            df = self.processed_doc._orderitem_obj._TableDataFrame
            self.check_order_items_row(
                df.iloc[0],
                {'item_number': '680109', 'shipped_quantity': '2', 'weight': '2.00',
                'price': '12.65', 'total_price': '25.30'}
            )
            self.check_order_items_row(
                df.iloc[1],
                {'item_number': '680459', 'shipped_quantity': '2', 'weight': '2.00',
                'price': '11.65', 'total_price': '23.30'}
            )
            self.check_order_items_row(
                df.iloc[2],
                {'item_number': '238040', 'shipped_quantity': '1', 'weight': '14.00',
                'price': '24.30'}
            )

# class FreshTest3(CommonTests, unittest.TestCase):
#     def setUp(self):
#         self.app = create_app(base)
#         self.response = file_load("../data/freshpoint/20200424_090212.jpg.json")
#         self.doc = Document(self.response)
        
#     def test_orders(self):
#         self.order = self.compute_order(self.doc.pages[0])
#         self.assertEqual(self.order.invoice_number, '1467251')
#         self.assertEqual(self.order.invoice_date, '2017-11-02')
#         self.assertEqual(self.order.customer_account_number, '605211')
    
#     def test_order_items(self):
#         with self.app.app_context():
#             self.processed_doc = ProcessedDocument(self.doc, '', '', '', 'freshpoint.json')
#             self.processed_doc.processDocument()
#             df = self.processed_doc._orderitem_obj._TableDataFrame
#             self.check_order_items_row(
#                 df.iloc[0],
#                 {'item_number': '212300', 'shipped_quantity': '1', 'weight': '10.00',
#                 'price': '50.85', 'total_price': '50.85'}
#             )
#             self.check_order_items_row(
#                 df.iloc[1],
#                 {'item_number': '680109', 'shipped_quantity': '1', 'weight': '1.00',
#                 'price': '12.50', 'total_price': '12.50'}
#             )
#             self.check_order_items_row(
#                 df.iloc[2],
#                 {'item_number': '202044', 'shipped_quantity': '6', 'weight': '12.00',
#                 'price': '4.55', 'total_price': '27.30'}
#             )

