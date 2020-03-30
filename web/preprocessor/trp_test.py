import json
from trp import Document
import pandas as pd
from utils import update_column_headers, convert_form_to_dict
from orders import Order
from orderitems import OrderitemsDF

def processDocument(doc):
    for page in doc.pages:
    #     print("PAGE\n====================")
    #     for line in page.lines:
    #         print("Line: {}--{}".format(line.text, ' '))
    #         for word in line.words:
    #             print("Word: {}--{}".format(word.text, ' '))
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

        # Turning invoice line items into a DF
        for table in page.tables:
            try:
                orderitems = OrderitemsDF()
                orderitems.set_orderitems_dataframe(table)
                df = orderitems.TableDataFrame
                import pdb; pdb.set_trace()
                # orderitems.convert_DF_to_Orderitem_objs()
            except KeyError:
                break
            

        # df = pd.DataFrame([[cell.text for cell in row.cells] for row in page.tables[0].rows])
        # orders_df = update_column_headers(df)
        # print(orders_df.head())
        # print(orders_df.columns)
        # print([line.text for line in page.lines])
        # print(orders_df.head())






def run():
    response = {}
    
    filePath = "./data/s3_responses/04eed195-04b7-40bd-a304-2609b8fd2db3.json" # <- First response we worked with
    # filePath = "./data/s3_responses/INV_044_17165_709955_20191106.PDF_3.png.json" # <- PDF response (1 of 4)  
    with open(filePath, 'r') as document:
        response = json.loads(document.read())

    doc = Document(response)
    processDocument(doc)

run()

