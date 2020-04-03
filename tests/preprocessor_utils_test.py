import json
import unittest
from web.preprocessor.trp import Document 

class TestStringMethods(unittest.TestCase):
    def test_document_upload(self):
        response = {}        
        filePath = "./data/s3_responses/04eed195-04b7-40bd-a304-2609b8fd2db3.json"
        with open(filePath, 'r') as document:
            response = json.loads(document.read())

        doc = Document(response)

if __name__ == '__main__':
    unittest.main()