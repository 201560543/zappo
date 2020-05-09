import pandas as pd
from io import StringIO
from flask import current_app
from datetime import datetime as dt
from flask_sqlalchemy import SQLAlchemy
from web.database import db
from web.preprocessor.constants import ORDER_HEADER_COLUMN_ORDER, DB_DATE_FORMAT
from web.preprocessor.utils import fetch_json, prefix_dictionary_search,\
    convert_form_to_dict, failover

class Order(db.Model):
    account_number = db.Column(db.String(32))
    invoice_number = db.Column(db.String(32), primary_key = True)
    invoice_term_name = db.Column(db.String(32))
    invoice_date = db.Column(db.String(32))
    supplier = db.Column(db.String(32))

    customer_account_number = db.Column(db.String(32))
    vendor = db.Column(db.String(32))
    order_items = db.Column(db.String(32))
    raw_sold_to_info = db.Column(db.String(32))
    invoice_subtotal = db.Column(db.String(32))

    def __init__(self, supplier_organization_number, account_number):
        self._Page = None
        self._Form_dict = None
        self.organization_number = supplier_organization_number
        self.account_number = account_number

    def __repr__(self):
        return '<Order {0}>'.format(self.invoice_number)

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

    def add_order_items(self, order_item):
        self.order_items.append(order_item)
    

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
                if isinstance(self.date_format, list):
                    for fmt in self.date_format:
                        try:
                            _date = dt.strptime(self.invoice_date, fmt)
                            self.invoice_date = dt.strftime(_date, DB_DATE_FORMAT)
                            break
                        except:
                            continue                        
                else:
                    _date = dt.strptime(self.invoice_date, self.date_format)
                    self.invoice_date = dt.strftime(_date, DB_DATE_FORMAT)
            else:
                # In case there is no date_format, then simply replace the characters.
                self.invoice_date = self.invoice_date.replace(" ","-")
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
        # Format Date
        self.format_date()
        # Perform validation
        self.validate()

        for k,v in self.__dict__.items():
            if k not in ['_Page', '_Form_dict']:
                print(k,':',v) 

    def set_attributes(self, data):
        for key, val in data.items():
            if hasattr(self, key):
                setattr(self, key, val)
    
    def validate(self):
        """
        Function to perform validation
        """
        assert self.invoice_number not in (None, 'None', '')

    def convert_to_tsv(self):
        """
        Used to export Header values as a tsv file. Returns both raw string format and buf
        """
        # TO DO: refactor - consider using avro in the future

        vals = []
        for key in ORDER_HEADER_COLUMN_ORDER:
            vals.append(self.__dict__.get(key))
        
        tsv_buf = StringIO()
        pd.DataFrame([vals], columns=ORDER_HEADER_COLUMN_ORDER).to_csv(path_or_buf=tsv_buf, sep='\t', header=True, index=False)
        raw_tsv = pd.DataFrame([vals], columns=ORDER_HEADER_COLUMN_ORDER).to_csv(path_or_buf=None, sep='\t', header=True, index=False)
        return tsv_buf, raw_tsv

