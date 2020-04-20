import json
import pandas as pd
from preprocessor.trp import Document
from preprocessor.utils import update_column_headers, convert_form_to_dict
from preprocessor.orders import Order
from preprocessor.orderitems import OrderitemsDF
pd.set_option('max_columns', 12)
pd.options.display.width = 0


class ProcessedDocument():
    """
    Class used to hold raw Document object from trp and processed outputs (buffer and tsv files for database upload)
    Buffer files are sent to S3, tsv is sent back to client
    Corresponding Account Number is stored as well in order to use as a prefix for S3 object key
    """

    def __init__(self, doc):
        self._raw_doc = doc
        self._order_buf = None
        self._order_tsv = None
        self._orderitem_buf = None
        self._orderitem_tsv = None
        self._account_number = None

    def set_order(self, order_buf, order_tsv):
        self._order_buf = order_buf
        self._order_tsv = order_tsv

    def set_orderitem(self, orderitem_buf, orderitem_tsv):
        self._orderitem_buf = orderitem_buf
        self._orderitem_tsv = orderitem_tsv
    
    def set_account_number(self, account_number):
        self._account_number = account_number

    def processDocument(self):
        for page in self._raw_doc.pages:
        #     print("PAGE\n====================")
            # for line in page.lines:
            #     print("Line: {}--{}".format(line.text, ' '))
            #     for word in line.words:
            #         print("Word: {}--{}".format(word.text, ' '))
        #     for table in page.tables:
        #         print("TABLE\n====================")
        #         for r, row in enumerate(table.rows):
        #             for c, cell in enumerate(row.cells):
        #                 print("Table[{}][{}] = {}-{}".format(r, c, cell.text, ' '))
        #     print("Form (key/values)\n====================")
        #     print('*'*20)
        #     for field in page.form.fields:
        #         k = ""
        #         v = ""
        #         if(field.key):
        #             k = field.key.text
        #         if(field.value):
        #             v = field.value.text
        #         print("Field: Key: {}, Value: {}".format(k,v))

        #     #Get field by key
        #     key = "Phone Number:"
        #     print("\nGet field by key ({}):\n====================".format(key))
        #     f = page.form.getFieldByKey(key)
        #     if(f):
        #         print("Field: Key: {}, Value: {}".format(f.key.text, f.value.text))


            #Search field by key
            # key = "CUSTOMER ACCOUNT NO."

            # fields = page.form.searchFieldsByKey(key)
            # print(page.form)
            # for field in fields:
            #     print("Field: Key: {}, Value: {}".format(field.key, field.value))
            # Getting Header Info
            print("==========================================")
            print("=========Header-Level Information=========")
            print("==========================================")
            order = Order()
            order.set_order_values(page)
            invoice_num = order._invoice_number
            supplier = order._supplier
            ## LINES BELOW TEMPORARY 
            TEMPORARY_ACCNT_NO = 'debddd37-82a9-11ea-b51c-0aedbe94' # Used to temporarily assign account until frontend can send accnt info
            order._account_number = TEMPORARY_ACCNT_NO # Order needs account number stored so it is stored as a column in the Memsql DB
            self.set_account_number(TEMPORARY_ACCNT_NO)
            ## LINES ABOVE TEMPORARY
            order_tsv_buf, order_header_raw_tsv = order.convert_to_tsv()
            self.set_order(order_tsv_buf, order_header_raw_tsv)
            # Turning invoice line items into a DF
            print("=============================================")
            print("=========Orderitem-Level Information=========")
            print("=============================================")
            for table in page.tables:
                try:
                    orderitems = OrderitemsDF()
                    orderitems.set_orderitems_dataframe(table)
                    df = orderitems.TableDataFrame
                    if df.empty:
                        continue
                    print(df)
                    print("Returning Preprocessed DataFrame and Headers")
                    # Setting header values in DataFrame of orderitems
                    orderitems.set_header_values(invoice_number=invoice_num, account_number=TEMPORARY_ACCNT_NO, supplier=supplier)
                    # Exporting as buffer and raw tsv
                    orderitems_tsv_buf, orderitems_raw_tsv = orderitems.export_items_as_tsv()
                    self.set_orderitem(orderitems_tsv_buf, orderitems_raw_tsv)
                    return 
                except KeyError:
                    pass

            # order = Order()
            # order.set_order_values(page)

            # df = pd.DataFrame([[cell.text for cell in row.cells] for row in page.tables[0].rows])
            # orders_df = update_column_headers(df)
            # print(orders_df.head())
            # print(orders_df.columns)
            # print([line.text for line in page.lines])
            # print(orders_df.head())
            # return 





def run():
    response = {}
    # # UPLOADED
    # TRUFFLES
    filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_709955_20191106-2.png.json"
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_744788_20191203-1.png.json"
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_750415_20191206-2.png.json" # Almost good, 1 line in broken not read
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_744788_20191203-2.png.json" # Almost good, 1 line in broken not read
    # FUUD
    # filePath = "../data/s3_responses_sysco/20191103_193403.jpg.json"
    # filePath = "../data/s3_responses/04eed195-04b7-40bd-a304-2609b8fd2db3.json" 
    # TRUFFLES TRUCK
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_20677_746612_20191204-2.png.json" # Good, but see why total price is missing for 1
    # TRUFFLES CAFE ANVIL CNTR
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_23905_725646_20191119-1.png.json" # Good, but investigate why size measure is gone for some rows
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_23905_725646_20191119-2.png.json"
    # OSCAR'S PUB
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_28773_750236_20191206-2.png.json"


    # filePath = "../data/s3_responses/INV_044_17165_709955_20191106.PDF_0.png.json" # <-- Combines lines
    # filePath = "../data/s3_responses_sysco/20191103_193232.jpg.json" # <-- Combines lines
    # filePath = "../data/s3_responses_sysco/20191103_193336.jpg.json" # <-- Isn't reading broken column
    # filePath = "../data/s3_responses_sysco/20191103_193346.jpg.json" # <-- Subtotal portion of invoice
    # filePath = "../data/s3_responses_sysco/20191103_193354.jpg.json" # <-- No data - End of invoice
    # filePath = "../data/s3_responses/INV_044_17165_709955_20191106.PDF_2.png.json" # <- no data. There are a few orderitems. Bad read
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_709955_20191106-1.png.json"  # <-- Combines lines
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_709955_20191106-4.png.json" # <-- Empty, end of invoice. no orderitems
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_709955_20191106-3.png.json" # <- no data. There are a few orderitems. Bad read
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_741819_20191130-2.png.json" # <-- Really bad read. Lots of data. Didn't capture tables
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_741819_20191130-3.png.json" # <-- Really bad read. Lots of data. Didn't capture tables
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_750415_20191206-1.png.json" # <-- Lots of available data. Textract didn't catch the table
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_741819_20191130-4.png.json" # <-- Subtotals. No relevant data. Still didn't capture tables though. Really bad read
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_741819_20191130-5.png.json" # <-- Empty, end of invoice
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_744788_20191203-3.png.json" # <-- Subtotals. No relevant data. Still didn't capture tables though. Really bad read
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_744788_20191203-4.png.json" # <-- Subtotals. No relevant data. Still didn't capture tables though. Really bad read
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_750415_20191206-3.png.json" # <-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_750415_20191206-4.png.json" #<-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_20677_709755_20191106-1.png.json" #<-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_20677_725235_20191119-1.png.json" #<-- Combines Lines
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_20677_725235_20191119-2.png.json" #<-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_20677_725235_20191119-3.png.json" #<-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_20677_746612_20191204-1.png.json" #<-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_20677_746612_20191204-3.png.json" # <-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_20677_746612_20191204-4.png.json" # <-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_23905_709646_20191106-1.png.json" # <-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_23905_709646_20191106-2.png.json" # <-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_23905_709646_20191106-3.png.json" # <-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_23905_725646_20191119-3.png.json" # <-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_23905_725646_20191119-4.png.json" # <-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_23905_748631_20191205-1.png.json" # <-- Combines lines
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_23905_748631_20191205-2.png.json" # <-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_23905_748631_20191205-3.png.json" # <-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_23905_748631_20191205-4.png.json" # <-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_28773_750236_20191206-1.png.json" # <-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_28773_750236_20191206-3.png.json" # <-- Empty
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_28773_750236_20191206-4.png.json" # <-- Subtotals, no line items

    # Attemping the same image several times for debugging
    # filePath = "../data/s3_responses_sysco/sysco_test_INV_044_17165_741819_20191130-1.png.json" # <-- Really bad read. Lots of data. Didn't capture tables
    # filePath =  "../data/s3_responses_sysco/retry/17165_741819_20191130-1_retry.json"
    # filePath =  "../data/s3_responses_sysco/retry/17165_741819_20191130-1_retry2.json"
    with open(filePath, 'r') as document:
        response = json.loads(document.read())

    doc = Document(response)
    processed_doc = ProcessedDocument(doc)
    processed_doc.processDocument()
    return processed_doc._orderitem_tsv

if __name__ == '__main__':
    run()