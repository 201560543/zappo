import unittest
import os
print(os.getcwd())
from web.preprocessor.trp import Document 

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_document_upload(self):
        response = {}        
        filePath = "./data/s3_responses/04eed195-04b7-40bd-a304-2609b8fd2db3.json"
        with open(filePath, 'r') as document:
            response = json.loads(document.read())

        doc = Document(response)

if __name__ == '__main__':
    unittest.main()