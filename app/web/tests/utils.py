import json
from web.models.orders import Order
from web.tests.constants import TEST_DIR, TEST_ACCNT_NUM, TEST_ORG_NUM


def file_load(file_name):
    with open(file_name, 'r') as document:
        return json.loads(document.read())

class CommonTests(object):
    def test_document_upload(self):
        self.assertTrue(self.response is not None)
        self.assertTrue(self.doc is not None)

    def test_document_pages(self):
        self.assertEqual(len(self.doc.pages), 1)

    def test_document_tables(self):
        first_page = self.doc.pages[0]
        self.assertEqual(len(first_page.tables) != 0, True)

    def compute_order(self, first_page, supplier_organization=TEST_ORG_NUM,\
                        account_number=TEST_ACCNT_NUM, template_name='freshpoint.json'):
        order = Order(supplier_organization_number=supplier_organization, 
                        account_number=account_number)
        order.set_order_values(first_page, template_name)
        return order
    
    def orders_details(self, invoice_number, invoice_date, customer_account_number):
        # Order needs to be set to use this
        self.assertEqual(self.order.invoice_number, invoice_number)
        self.assertEqual(self.order.invoice_date, invoice_date)
        self.assertEqual(self.order.customer_account_number, customer_account_number)

    def check_order_items_row(self, row, measures):
        for k, v in measures.items():
            self.assertEqual(row[k], v)