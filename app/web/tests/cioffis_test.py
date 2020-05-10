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
        self.orders_details('932312', '2018-02-02', '1561')
    
    def test_orders_incorrect_template(self):
        with self.assertRaises(Exception):
            self.compute_order(self.doc.pages[0], template_name='freshpoint.json')
    
    def test_order_items(self):
        with self.app.app_context():
            self.processed_doc = ProcessedDocument(self.doc, '', '', '', 'cioffi.json')
            self.processed_doc.processDocument()
            df = self.processed_doc._orderitem_obj._TableDataFrame
            self.check_order_items_row(
                df.iloc[0],
                {'item_number': 's00951', 'shipped_quantity': '19.18', 'price': '10.99', 'total_price': '210.79'}
            )

class Cioffis2(CommonTests, unittest.TestCase):
    def setUp(self):
        self.app = create_app(base)
        self.response = file_load("../data/cioffis/20191103_193427.jpg.json")
        self.doc = Document(self.response)
        
    def test_orders(self):
        self.order = self.compute_order(self.doc.pages[0], template_name='cioffi.json')
        self.orders_details('933326', '2018-02-15', '1561')
    
    def test_order_items(self):
        with self.app.app_context():
            self.processed_doc = ProcessedDocument(self.doc, '', '', '', 'cioffi.json')
            self.processed_doc.processDocument()
            df = self.processed_doc._orderitem_obj._TableDataFrame
            # First row
            self.check_order_items_row(
                df.iloc[0],
                {'item_number': 'ws00122', 'shipped_quantity': '98',
                'price': '24.30', 'total_price': '23.81'}
            )
            # Second row
            self.check_order_items_row(
                df.iloc[1],
                {'item_number': '854693000010', 'shipped_quantity': '36',
                'price': '2.511', 'total_price': '90.40'}
            )

