import json
import unittest
from web.preprocessor.trp import Document 
from web.models.orders import Order 
from web.tests.constants import TEST_DIR, TEST_ACCNT_NUM, TEST_ORG_NUM

# For testing purposes, so that it can run normally
# we have to update the directory to conform in the same way
# as the flask application.
import os
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class OrderClassTest(unittest.TestCase):
    def setUp(self):
        """
        Function to setup the base for the test cases
        """
        filePath = "../data/s3_responses/04eed195-04b7-40bd-a304-2609b8fd2db3.json"
        with open(filePath, 'r') as document:
            self.response = json.loads(document.read())
         

    def test_document_upload(self):
        """
        Test response upload and test if the Document class can ingest the JSON data
        """
        self.assertTrue(self.response is not None)
        doc = Document(self.response)
        self.assertTrue(doc is not None)

    def test_order_object(self):
        """
        Test the entries in orders
        """
        doc = Document(self.response)
        first_page = doc.pages[0]
        order = Order(supplier_organization_number = TEST_ORG_NUM, 
                            account_number=TEST_ACCNT_NUM)
        order.set_order_values(first_page)

        self.assertEqual(order.customer_account_number, '25651')
        self.assertEqual(order.invoice_number, '9897186')
        self.assertTrue(order.raw_sold_to_info.startswith('fuud foods inc.'))

    def test_order_object_with_another_file(self):
        """
        Test the entries in orders
        """

        resp = {}
        with open("../data/s3_responses/INV_044_17165_709955_20191106.PDF_0.png.json", 'r') as document:
            resp = json.loads(document.read())
        doc = Document(resp)
        first_page = doc.pages[0]
        with self.assertRaises(Exception):
            order = Order()
            order.set_order_values(first_page)

        self.assertEqual(order.customer_account_number, '17165')
        self.assertEqual(order.invoice_number, '709955')
        self.assertTrue(order.raw_sold_to_info.startswith('TRUFFLES FINE FOODS LTD'))


    def tearDown(self):
        del self.response
