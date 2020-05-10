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


class Cioffis3(CommonTests, unittest.TestCase):
    def setUp(self):
        self.app = create_app(base)
        self.response = file_load("../data/cioffis/20200420_200550.jpg.json")
        self.doc = Document(self.response)
        
    def test_orders(self):
        self.order = self.compute_order(self.doc.pages[0], template_name='cioffi.json')
        self.orders_details('794041', '2016-10-28', '1561')
    
    def test_order_items(self):
        with self.app.app_context():
            self.processed_doc = ProcessedDocument(self.doc, '', '', '', 'cioffi.json')
            self.processed_doc.processDocument()
            df = self.processed_doc._orderitem_obj._TableDataFrame
            # First row
            self.check_order_items_row(
                df.iloc[0],
                {'item_number': '0348', 'shipped_quantity': '.335',
                'price': '3.14', 'total_price': '1.05'}
            )
            # Second row
            self.check_order_items_row(
                df.iloc[1],
                {'item_number': 'ws00106', 'shipped_quantity': '43',
                'price': '29.99', 'total_price': '12.90'}
            )
            # Third row
            self.check_order_items_row(
                df.iloc[2],
                {'item_number': 'ws2250', 'shipped_quantity': '3',
                'price': '4.99', 'total_price': '14.97'}
            )
            # Fourth row
            self.check_order_items_row(
                df.iloc[3],
                {'item_number': 'ws00075', 'shipped_quantity': '4.56',
                'price': '9.24', 'total_price': '42.13'}
            )
            # Fifth row
            self.check_order_items_row(
                df.iloc[4],
                {'item_number': 'ws1309', 'shipped_quantity': '6.85',
                'price': '9.99', 'total_price': '68.43'}
            )
            # Sixth row
            self.check_order_items_row(
                df.iloc[5],
                {'item_number': 'cb1416', 'shipped_quantity': '2',
                'price': '5.11', 'total_price': '10.22'}
            )
            # Seventh row
            self.check_order_items_row(
                df.iloc[6],
                {'item_number': 'ws00081', 'shipped_quantity': '1',
                'price': '15.99', 'total_price': '15.99'}
            )
            # Eight row
            self.check_order_items_row(
                df.iloc[7],
                {'item_number': 'ws1314', 'shipped_quantity': '225',
                'price': '18.99', 'total_price': '4.27'}
            )
            # Ninth row
            self.check_order_items_row(
                df.iloc[8],
                {'item_number': 'ws00014', 'shipped_quantity': '2',
                'price': '47.79', 'total_price': '95.58'}
            )
            # Tenth row
            self.check_order_items_row(
                df.iloc[9],
                {'item_number': 'ws3241', 'shipped_quantity': '.5',
                'price': '9.99', 'total_price': '5.00'}
            )
            # Last row
            self.check_order_items_row(
                df.iloc[10],
                {'item_number': '8030853001048', 'shipped_quantity': '1',
                'price': '12.861', 'total_price': '12.86'}
            )

