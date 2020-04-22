import copy 
import pandas as pd
from typing import List
from datetime import datetime as dt
from preprocessor.utils import fetch_json, prefix_dictionary_search, convert_form_to_dict, failover
from preprocessor.constants import ORDER_HEADER_COLUMN_ORDER, DB_DATE_FORMAT
from io import StringIO
from flask import current_app

class Order():
    def __init__(self):
        self._Page = None
        self._Form_dict = None

        self._account_number = None # ZappoTrack accnt number
        self._invoice_number = None
        self._invoice_term_name = None
        self._invoice_date = None
        self._supplier = None

        self._customer_account_number = None # Customer's accnt number with supplier
        self._order_items = []
        self._raw_sold_to_info = None


    def __str__(self):
        return f'{self._invoice_number}, number of items: {len(self._order_items)}'

    @property
    def Page(self):
        return self._Page
	
    @Page.setter
    def Page(self,page_obj):
        self._Page = page_obj
        self._Form_dict = convert_form_to_dict(page_obj.form)

    @property
    def Form_dict(self):
        return self._Form_dict

    @property
    def invoice_number(self):
        return self._invoice_number

    @property
    def invoice_term_name(self):
        return self._invoice_term_name

    @property
    def customer_account_number(self):
        return self._customer_account_number

    @property
    def invoice_date(self):
        return self._invoice_date

    @property
    def order_items(self):
        return [order_item for order_item in self._order_items]

    @property
    def raw_sold_to_info(self):
        return self._raw_sold_to_info

    @property
    def supplier(self):
        return self._supplier

    def add_order_items(self, order_item):
        self._order_items.append(order_item)

    def set_order_template(self, template_name):
        """
        Function to set the order template
        """
        # Fetch the required template type
        template_data = fetch_json(template_name)
        # Fetch the order and date template
        self.order_template = template_data.get('mapper').get('order')
        self.date_format = template_data.get('date_format')

    def extract_keys_using_template(self):
        """
        Extract keys from Page object's Form Fields, search template for matches, and return matches with their corresponding indices
        """
        order_template = self.order_template
        # For each extracted key, search for relevant keys from the json template
        matched_keys_raw = {prefix_dictionary_search(field_key, order_template):self.Form_dict[field_key]
                            for field_key, val
                            in self.Form_dict.items()
                            if val is not None}

        # Remove all empty keys
        del matched_keys_raw['']

        return {**matched_keys_raw, **failover(matched_keys_raw, order_template, self._Page)}
    
    def format_date(self):
        """
        Textract may read dates as "YYY MM DD". Reformat to "YYYY-MM-DD" for DB insertion.
        If our template provides a date format then use it for conversion.
        """
        try:
            if self.date_format:
                self._invoice_date = dt.strptime(self._invoice_date, self.date_format)
                self._invoice_date = dt.strftime(DB_DATE_FORMAT, self._invoice_date)
            else:
                # In case there is no date_format, then simply replace the characters.
                self._invoice_date = self._invoice_date.replace(" ","-")
        except:
            current_app.logger.warning("Invoice date was not picked.")

    def set_order_values(self, page_obj, template_name = 'sysco.json'):
        # Set the order template to the class
        self.set_order_template(template_name)
        # Set Page object
        self.Page = page_obj
        # Get Page's Form 
        searched_form_dict = self.extract_keys_using_template()
        # Set attributes using extracted keys
        self.set_attributes(searched_form_dict)
        # Set supplier using template
        self._supplier = template_name[:-5]
        # Format Date
        self.format_date()

        for k,v in self.__dict__.items():
            if k not in ['_Page', '_Form_dict']:
                print(k,':',v) 

    def set_attributes(self, data):
        for key, val in data.items():
            if hasattr(self, key):
                setattr(self, f'_{key}', val)

    def convert_to_tsv(self):
        """
        Used to export Header values as a tsv file. Returns both raw string format and buf
        """
        # TO DO: refactor - consider using avro in the future

        vals = []
        for key in ORDER_HEADER_COLUMN_ORDER:
            key_prefixed = '_'+key
            vals.append(self.__dict__.get(key_prefixed))
        
        tsv_buf = StringIO()
        pd.DataFrame([vals]).to_csv(path_or_buf=tsv_buf, sep='\t', header=False, index=False)
        raw_tsv = pd.DataFrame([vals]).to_csv(path_or_buf=None, sep='\t', header=False, index=False)
        return tsv_buf, raw_tsv

