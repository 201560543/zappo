import json
import unittest
from web.preprocessor.trp import Document 

class TrpClassTest(unittest.TestCase):
    def setUp(self):
        """
        Function to setup the base for the test cases
        """
        filePath = "./data/s3_responses/04eed195-04b7-40bd-a304-2609b8fd2db3.json"
        with open(filePath, 'r') as document:
            self.response = json.loads(document.read())
         

    def test_document_upload(self):
        """
        Test response upload and test if the Document class can ingest the JSON data
        """
        self.assertTrue(self.response is not None)
        doc = Document(self.response)
        self.assertTrue(doc is not None)

    def test_document_pages(self):
        """
        Test the number of pages that were received in the JSON
        """
        doc = Document(self.response)
        self.assertEqual(len(doc.pages), 1)


    def tearDown(self):
        del self.response
